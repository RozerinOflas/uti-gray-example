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
        print(self.request.data)
        self.request.model = PackageModel(**(self.request.data))
        self.kernelSize = self.request.get_param("kernelSize", 3)
        print(self.kernelSize)
        self.parameters()
        self.blurTypes = self.request.get_param("blurrTypes", None)
        self.sigmaX = self.request.get_param("sigmaX")
        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def parameters(self):
        if self.kernelSize == "kernelSize5x5":
            self.kernelSize = 5
        elif self.kernelSize == "kernelSize3x3":
            self.kernelSize = 3
        else:
            self.kernelSize = 7

        print("load_self.kernelSize:", self.kernelSize)
        return self.kernelSize

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)

        if self.blurTypes.lower() == "blurrgaussian":
            img.value = cv2.GaussianBlur(img.value, (self.kernelSize, self.kernelSize), self.sigmaX)

        elif self.blurTypes.lower() == "blurrmedian":
            img.value = cv2.medianBlur(img.value, self.kernelSize)

        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response2(context=self)
        return packageModel

if __name__ == "__main__":
    Executor(sys.argv[1]).run()
