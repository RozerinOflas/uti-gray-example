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
        self.blurTypes = self.request.get_param("BlurTypes")
        if self.blurTypes is None:
            raise ValueError("Blur requires 'blurTypes' parameter.")
        self.kernelSize = self.request.get_param("KernelSize")
        if self.kernelSize is None:
            raise ValueError("Blur requires 'kernelSize' parameter.")
        self.sigmaX = self.request.get_param("SigmaX")
        if self.sigmaX is None:
            raise ValueError("Blur requires 'sigmaX' parameter.")
        self.image = self.request.get_param("inputImage")
        if self.image is None:
            raise ValueError("Blur requires 'image' parameter.")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}
    def blur(self,kernelSize, sigmaX, image, blurTypes):
        if self.blurTypes == "gaussian":
            return cv2.GaussianBlur(image, (kernelSize, kernelSize), sigmaX).astype(np.uint8)
        elif self.blurTypes == "median":
            return cv2.medianBlur(image, kernelSize).astype(np.uint8)
        else:
            raise ValueError(f"Unknown blurType: {blurTypes}")

    def run(self):
        img = Image.get_frame(self.image, redis_db=self.redis_db)
        # KernelSize string'den int'e çevirme (örn. "Kernel3x3" -> 3)
        if isinstance(self.kernelSize, str) and self.kernelSize.lower().startswith("kernel"):
            try:
                kernel_size_int = int(self.kernelSize[-3])  # 3, 5, 7 gibi
            except Exception:
                kernel_size_int = 3
        else:
            kernel_size_int = int(self.kernelSize)

        blurred_img = self.blur(
            kernel_size_int,
            int(self.sigmaX),
            img.value,
            self.blurTypes.lower()
        )

        img.value = blurred_img
        self.image = Image.set_frame(img.value, package_uID=self.uID, redis_db=self.redis_db)
        response = build_responseblur(self.image)
        return response

    if "__main__" == __name__:
        Executor(sys.argv[1]).run()