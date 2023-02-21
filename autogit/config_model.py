from typing import Dict
from pydantic import BaseModel
from pathlib import Path

class AutoGitConfig(BaseModel):
    task: str
    root_dir: Path
    config_dir: Path # contains folders with task names containing autogit.yaml files
    working_dir: Path
    # the following 3 are set by CMDInitBareRepo.execute()
    bare_dir: Path = None
    repo_dir: Path = None
    current_repo: str = None
    authors: Dict[str, str]
    emails: Dict[str, str]
