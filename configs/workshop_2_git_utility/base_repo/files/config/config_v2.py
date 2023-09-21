from pydantic import BaseModel, validator


class Config(BaseModel):

    PROJECT_NAME: str = "PW-ULTIMATE"
    """offical name of this project as decided by marketing"""

    USE_SPECIAL_CHARACTERS: bool = True
    """flag to control whether special characters are used in the generated passwords"""
    
    DEFAULT_PASSWORD_LENGTH: int = 10
    """base characters used for all passwords"""

    @validator("DEFAULT_PASSWORD_LENGTH")
    def check_pwd_length(cls, value, values):
        if value < 5:
            raise ValueError("DEFAULT_PASSWORD_LENGTH cannot be set to values smaller than 5")
        return value
