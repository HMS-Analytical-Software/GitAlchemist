from typing import Dict
from pydantic import BaseModel
from pathlib import Path

class AutoGitConfig(BaseModel):
    task: str
    root_dir: Path
    config_dir: Path
    #working_dir: Path
    current_repo: str = None # is set by init_bare_repo function!
    authors: Dict[str, str]
    emails: Dict[str, str]
