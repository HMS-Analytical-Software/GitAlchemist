from pydantic import BaseModel


class Config(BaseModel):

    PROJECT_NAME: str = "PW-ULTIMATE"
    """offical name of this project as decided by marketing"""

    USE_SPECIAL_CHARACTERS: bool = True
    """flag to control whether special characters are used in the generated passwords"""

    DEFAULT_PASSWORD_LENGTH: int = 10
    """base characters used for all passwords"""
