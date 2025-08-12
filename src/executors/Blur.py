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

        self.blur_type = self.request.get_param("blurTypes", "BlurrGaussian")
        self.kernelSize = self.request.get_param("kernelSize", 3)
        self.sigmaX = self.request.get_param("sigmaX", 0)

        try:
            self.kernelSize = int(self.kernelSize)
            if self.kernelSize % 2 == 0:
                self.kernelSize += 1
        except Exception:
            self.kernelSize = 3

        try:
            self.sigmaX = float(self.sigmaX)
        except Exception:
            self.sigmaX = 0.0

        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        if self.blur_type.lower() == "blurrGaussian":
            img.value = cv2.GaussianBlur(img.value, (self.kernelSize, self.kernelSize), self.sigmaX)

        elif self.blur_type.lower() == "blurrMedian":
            img.value = cv2.medianBlur(img.value, self.kernelSize)

        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response2(context=self)
        return packageModel

if __name__ == "__main__":
    Executor(sys.argv[1]).run()
