import os
import cv2
import sys

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
        return cv2.resize(image, (self.width, self.height))

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.scaling(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)

        imgA = Image.get_frame(img=self.imageA, redis_db=self.redis_db)
        imgA.value = self.scaling(imgA.value)
        self.imageA = Image.set_frame(img=imgA, package_uID=self.uID, redis_db=self.redis_db)

        print("img type:", type(img), "img.value type:", type(img.value))
        print("img2 type:", type(imgA), "img2.value type:", type(imgA.value))


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
