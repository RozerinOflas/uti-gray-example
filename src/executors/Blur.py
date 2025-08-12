import os
import cv2
import sys
import numpy as np
import base64

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GrayExample.src.utils.response import build_responseblur
from components.GrayExample.src.models.PackageModel import PackageModel

class Blur(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.blurTypes = self.request.get_param("blurTypes")
        if self.blurTypes is None:
            raise ValueError("Blur requires 'blurTypes' parameter.")
        self.kernelSize = self.request.get_param("kernelSize")
        if self.kernelSize is None:
            raise ValueError("Blur requires 'kernelSize' parameter.")
        self.sigmaX = self.request.get_param("sigmaX")
        if self.sigmaX is None:
            raise ValueError("Blur requires 'sigmaX' parameter.")
        self.image = self.request.get_param("image")
        if self.image is None:
            raise ValueError("Blur requires 'image' parameter.")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}
    def blur(self,kernelSize, sigmaX, image):
        if self.blurTypes == "gaussian":
            return cv2.GaussianBlur(image, (kernelSize, kernelSize), sigmaX).astype(np.uint8)
        elif self.blurTypes == "median":
            return cv2.medianBlur(image, kernelSize).astype(np.uint8)

    def run(self):
        img= Image.get_frame(self.image, redis_db=self.redis_db)
        img.value=self.blur(img.value)
        self.image = Image.set_frame(img.value, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_responseblur
        return packageModel

    if "__main__" == __name__:
        Executor(sys.argv[1]).run()