
from sdks.novavision.src.helper.package import PackageHelper
from components.GrayExample.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, GrayExampleExecutorOutputs, GrayExampleExecutorResponse, GrayExampleExecutor, OutputImage


def build_response(context):
    outputImage = OutputImage(value=context.image)
    GrayExampleExecutorOutputs = GrayExampleExecutorOutputs(outputImage=outputImage)
    GrayExampleExecutorResponse = GrayExampleExecutorResponse(outputs=GrayExampleExecutorOutputs)
    GrayExampleExecutorExecutor = GrayExampleExecutorExecutor(value=GrayExampleExecutorResponse)
    executor = ConfigExecutor(value=GrayExampleExecutorExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel