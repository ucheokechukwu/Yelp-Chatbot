from pydantic import BaseModel
class YelpQueryInput(BaseModel):
    text: str
class YelpQueryOutput(BaseModel):
    input_: str
    output_: str
    intermediate_steps: list[str]