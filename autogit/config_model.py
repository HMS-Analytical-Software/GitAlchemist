from typing import Dict
from pydantic import BaseModel


class AutoGitConfig(BaseModel):
    task: str
    root_dir: str
    working_dir: str
    current_repo: str = None # is set by init_bare_repo function!
    authors: Dict[str, str]
    emails: Dict[str, str]
