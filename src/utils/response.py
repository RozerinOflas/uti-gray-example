
from sdks.novavision.src.helper.package import PackageHelper
from components.GrayExample.src.models.PackageModel import PackageModel, PackageConfigs,ConfigExecutor, GrayExampleExecutor, GrayExampleExecutorOutputs, GrayExampleExecutorResponse, Gray2, Gray2Outputs, Gray2Response,OutputImage


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
    gray2Outputs = Gray2Outputs(outputImage=outputImage)
    gray2Response = Gray2Response(outputs=gray2Outputs)
    gray2 = Gray2(value=gray2Response)
    executor = ConfigExecutor(value=gray2)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel