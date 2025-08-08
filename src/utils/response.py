
from sdks.novavision.src.helper.package import PackageHelper
from components.GrayExample.src.models.PackageModel import PackageModel, PackageConfigs,ConfigExecutor, GrayExampleExecutor, GrayExampleExecutorOutputs, GrayExampleExecutorResponse, OutputImage


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