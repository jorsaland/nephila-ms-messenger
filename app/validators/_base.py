"""
Defines the base for the validation models.
"""


from pydantic import BaseModel, ConfigDict, model_validator


class BaseValidationModel(BaseModel):

    """
    Base for the validation models.
    """

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode='before')
    @classmethod
    def treat_none_as_missing(cls, data):
        if not isinstance(data, dict):
            return data
        return {key: value for key, value in data.items() if value is not None}