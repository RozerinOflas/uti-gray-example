import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GrayExample.src.utils.response import build_response2
from components.GrayExample.src.models.PackageModel import PackageModel


class BlurrGaussian:
    def __init__(self, KernelSize=3):
        if KernelSize % 2 == 0:
            KernelSize += 1
        self.KernelSize = KernelSize

    def apply(self, img):
        return cv2.GaussianBlur(img, (self.KernelSize, self.KernelSize), 0)


class BlurrMedian:
    def __init__(self, KernelSize=3):
        if KernelSize % 2 == 0:
            KernelSize += 1
        self.KernelSize = KernelSize

    def apply(self, img):
        return cv2.medianBlur(img, self.KernelSize)


class Blur(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.blur_type = self.request.get_param("blurType")
        self.KernelSize = int(self.request.get_param("KernelSize", 3))
        self.image = self.request.get_param("inputImage")

        if self.blur_type == "Gaussian":
            self.blurr = BlurrGaussian(self.KernelSize)
        elif self.blur_type == "Median":
            self.blurr = BlurrMedian(self.KernelSize)

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def bluring(self, img):
        if self.blurr:
            return self.blurr.apply(img)
        else:
            return img

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.bluring(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response2(context=self)
        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
