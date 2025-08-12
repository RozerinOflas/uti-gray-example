import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GrayExample.src.utils.response import build_response2
from components.GrayExample.src.models.PackageModel import PackageModel


class Blur(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        # Parametreleri net şekilde alıyoruz:
        self.blur_type = self.request.get_param("blurType")  # Örn: "Gaussian" veya "Median"
        self.kernel_size = self.request.get_param("kernelSize", 3)  # Örn: 3, 5, 7 gibi tek sayı
        self.image = self.request.get_param("inputImage")

        # Kernel boyutunu tek sayı yapalım (bazı blurlar için zorunlu)
        if self.kernel_size % 2 == 0:
            self.kernel_size += 1

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def bluring(self, img):
        if self.blur_type == "Gaussian":
            # GaussianBlur kernel boyutu tuple olarak verilir
            img = cv2.GaussianBlur(img, (self.kernel_size, self.kernel_size), 0)
        elif self.blur_type == "Median":
            img = cv2.medianBlur(img, self.kernel_size)
        else:
            # Bilinmeyen blur tipi gelirse resmi değiştirmeden döndür
            pass
        return img

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.bluring(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response2(context=self)
        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
