from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"
class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class Degree(Config):
    """
        Positive degree input
    """
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359.0, le=359.0,default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[-359, 359]"] = "[-359, 359]"

    class Config:
        title = "Degreee"

class Width(Config):
    """
        Positive width input
    """
    name: Literal["Width"] = "Width"
    value: int = Field(ge=-359.0, le=359.0,default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[-359, 359]"] = "[-359, 359]"

    class Config:
        title = "Width"

class Height(Config):
    """
        Positive height input
    """
    name: Literal["Height"] = "Height"
    value: int = Field(ge=-359.0, le=359.0,default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[-359, 359]"] = "[-359, 359]"

    class Config:
        title = "Height"




class KeepSideFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"
class KeepSideTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"
class KeepSideBBox(Config):
    """
        Rotate image without catting off sides.
    """
    name: Literal["KeepSide"] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Keep Sides"


class BlurrMedian(Config):
    """
        Positive
    """
    name: Literal["BlurrMedian"] = "BlurrMedian"
    value: Literal["BlurrMedian"] = "BlurrMedian"
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "BlurrMedian"
class BlurrGaussian(Config):
    """
        Positive angles specify counterclockwise rotation while negative angles indicate clockwise rotation.
    """
    name: Literal["BlurrGaussian"] = "BlurrGaussian"
    value: Literal["BlurrGaussian"] = "BlurrGaussian"
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "BlurrGaussian"


class BlurTypes(Config):
    name: Literal["BlurTypes"] = "BlurTypes"
    value: Union[BlurrGaussian, BlurrMedian]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "BlurTypes"



class GrayExampleExecutorInputs(Inputs):
    inputImage: InputImage
class GrayExampleExecutorConfigs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox
class GrayExampleExecutorRequest(Request):
    inputs: Optional[GrayExampleExecutorInputs]
    configs: GrayExampleExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }
class GrayExampleExecutorOutputs(Outputs):
    outputImage: OutputImage
class GrayExampleExecutorResponse(Response):
    outputs: GrayExampleExecutorOutputs


class BlurInputs(Inputs):
    inputImage: InputImage
class BlurConfigs(Configs):
    blurTypes:BlurTypes
class BlurRequest(Request):
    inputs: Optional[BlurInputs]
    configs: BlurConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }
class BlurOutputs(Outputs):
    outputImage: OutputImage
class BlurResponse(Response):
    outputs: BlurOutputs


class ScallingInputs(Inputs):
    inputImage: InputImage
class ScallingConfigs(Configs):
    width:Width
    height:Height
class ScallingRequest(Request):
    inputs: Optional[ScallingInputs]
    configs: ScallingConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }
class ScallingOutputs(Outputs):
    outputImage: OutputImage
class ScallingResponse(Response):
    outputs: ScallingOutputs


class GrayExampleExecutor(Config):
    name: Literal["GrayExampleExecutor"] = "GrayExampleExecutor"
    value: Union[GrayExampleExecutorRequest, GrayExampleExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Rotation"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }
class Blur(Config):
    name: Literal["Blur"] = "Blur"
    value: Union[BlurRequest, BlurResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Blur"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[GrayExampleExecutor,Blur,Scalling]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Type"
class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["GrayExample"] = "GrayExample"
