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
        self.height = int(self.request.get_param("Height"))
        self.image = self.request.get_param("inputImage")
        self.imageA = self.request.get_param("inputImageA")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def scaling(self, image):
        if image is None:
            raise ValueError("Empty image data cannot be processed.")

        # Base64 string veya bytes ise decode et
        if isinstance(image, (str, bytes)):
            if isinstance(image, str):
                image = image.encode()
            img_data = base64.b64decode(image)
            np_arr = np.frombuffer(img_data, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if image is None or image.size == 0:
                raise ValueError("Decoded image is empty or invalid.")

        if not isinstance(image, np.ndarray):
            raise ValueError("Input to scaling must be base64 string, bytes or ndarray")

        # Orijinal boyutlar
        orig_height, orig_width = image.shape[:2]

        # Kullanıcının verdiği hedef boyutlar
        max_width, max_height = self.width, self.height

        # Orijinal en-boy oranı
        aspect_ratio = orig_width / orig_height

        # Önce max_width ve max_height değerlerine göre bir hedef boyut belirle
        # Burada orijinal en-boy oranını koruyarak boyutları küçültüyoruz
        if (max_width / aspect_ratio) <= max_height:
            # Genişlik sınırına göre yeniden boyutlandır
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            # Yükseklik sınırına göre yeniden boyutlandır
            new_height = max_height
            new_width = int(max_height * aspect_ratio)

        resized = cv2.resize(image, (new_width, new_height))
        return resized

    def run(self):

        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        if img.value is None:
            raise ValueError("img.value is None! ")

        img.value = self.scaling(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)

        imgA = Image.get_frame(img=self.imageA, redis_db=self.redis_db)
        if imgA.value is None:
            raise ValueError("imgA.value is None! ")

        imgA.value = self.scaling(imgA.value)
        self.imageA = Image.set_frame(img=imgA, package_uID=self.uID, redis_db=self.redis_db)


        packageModel = build_responseScale(context=self)
        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
