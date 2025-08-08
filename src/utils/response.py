
from sdks.novavision.src.helper.package import PackageHelper
from components.GrayExample.src.models.PackageModel import PackageModel, PackageConfigs,ConfigExecutor, GrayExampleExecutor, GrayExampleExecutorOutputs, GrayExampleExecutorResponse, Blur, BlurOutputs, BlurResponse, Scalling, ScallingOutputs,ScallingResponse,OutputImage,OutputImageA


def build_response(context):
    outputImage = OutputImage(value=context.image)
    grayExampleExecutorOutputs = GrayExampleExecutorOutputs(outputImage=outputImage)
    grayExampleExecutorResponse = GrayExampleExecutorResponse(outputs=grayExampleExecutorOutputs)
    grayExampleExecutor = GrayExampleExecutor(value=grayExampleExecutorResponse)
    executor = ConfigExecutor(value=grayExampleExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_response2(context):
    outputImage = OutputImage(value=context.image)
    blurOutputs = BlurOutputs(outputImage=outputImage)
    blurResponse = BlurResponse(outputs=blurOutputs)
    blur = Blur(value=blurResponse)
    executor = ConfigExecutor(value=blur)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_responseScale(context):
    outputImage = OutputImage(value=context.image)
    outputImageA = OutputImageA(value=context.image)
    scallingOutputs = ScallingOutputs(outputImage=outputImage)
    scallingResponse = ScallingResponse(outputs=scallingOutputs)
    scalling = Scalling(value=scallingResponse)
    executor = ConfigExecutor(value=scalling)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel