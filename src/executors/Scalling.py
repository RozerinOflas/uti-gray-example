
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
        self.rotation_degree = self.request.get_param("Degree")
        self.blurTypes = self.request.get_param("blurTypes")
        print("self.blurTypes = ", self.blurTypes)
        self.image = self.request.get_param("inputImage")
    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}


    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.Bluring(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_responseScale(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()