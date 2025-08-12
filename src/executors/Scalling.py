import os
import cv2
import sys
import numpy as np
import base64

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GrayExample.src.utils.response import build_responseScale
from components.GrayExample.src.models.PackageModel import PackageModel


class Scalling(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.width = int(self.request.get_param("Width"))
        print("width:", self.width)
        self.height = int(self.request.get_param("Height"))
        print("height:", self.height)
        self.image = self.request.get_param("inputImage")
        self.imageA = self.request.get_param("inputImageA")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def scaling(self, image):
        if not image:
            raise ValueError("Empty image data cannot be processed.")
        if isinstance(image, (str, bytes)):
            if isinstance(image, str):
                image = image.encode()
            img_data = base64.b64decode(image)
            np_arr = np.frombuffer(img_data, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            resized = cv2.resize(image, (self.width, self.height))
            return resized
        else:
            raise ValueError("Input to scaling must be base64 string or bytes")

    def run(self):
        print("inputImage param:", self.image)
        print("inputImageA param:", self.imageA)

        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        print("img.value after get_frame:", type(img.value))
        if img.value is None:
            raise ValueError("img.value is None! inputImage parametresi eksik veya yanlış formatta.")

        img.value = self.scaling(img.value)  # ndarray döner
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)

        imgA = Image.get_frame(img=self.imageA, redis_db=self.redis_db)
        print("imgA.value after get_frame:", type(imgA.value))
        if imgA.value is None:
            raise ValueError("imgA.value is None! inputImageA parametresi eksik veya yanlış formatta.")

        imgA.value = self.scaling(imgA.value)  # ndarray döner
        self.imageA = Image.set_frame(img=imgA, package_uID=self.uID, redis_db=self.redis_db)

        print("img type:", type(img), "img.value type:", type(img.value))
        print("imgA type:", type(imgA), "imgA.value type:", type(imgA.value))

        packageModel = build_responseScale(context=self)
        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
