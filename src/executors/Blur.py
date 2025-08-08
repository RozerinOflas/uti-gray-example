
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
        self.blurTypes = self.request.get_param("blurTypes")
        print("self.blurTypes = ", self.blurTypes)
        self.image = self.request.get_param("inputImage")
    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def Bluring(self,img):
        if self.blurTypes==BlurrGaussian:
            img = cv2.GaussianBlur(img,self.blurTypes)
        elif self.blurTypes==BlurrMedian:
            img = cv2.medianBlur(img,self.blurTypes)
        return

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.Bluring(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response2(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()