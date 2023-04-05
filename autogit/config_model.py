from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel


class AutoGitConfig(BaseModel):
    """
    Represents the configuration of an AutoGit task and is shared between its commands. 
    It contains information on different paths that are needed for repository generation 
    and git command execution. 

    Fields:
    - task (str): the task name. This is equivalent to the directory containing the autogit.yaml file in config_dir.
    - root_dir (Path): top-level directory. 
    - config_dir (Path): directory containing task directories (field 'task') of name task. 
    - working_dir (Path): directory where git repositories should be built. Should be a path that is relative to root_dir. 
      Will be created as a subdirectory of root_dir. 

    - bare_dir (Path): directory of a bare repository to clone from and push to, which is the first step in all AutoGit tasks. 
      Is provided by autogit.yaml configuration file and set by CMDInitBareRepo. 
    - repo_dir (Path): directory of the git repository that is active in a task. 
      Is provided by autogit.yaml configuration file and set by CMDInitBareRepo. 
    - current_repo (str): name of the currently active git repository. 
      Is provided by autogit.yaml and set by CMDInitBareRepo. 
    - authors, emails: data necessary for git config. 
    """
    task: str
    root_dir: Path
    config_dir: Path
    working_dir: Path
    bare_dir: Path = None
    repo_dir: Path = None
    current_repo: str = None
    authors: Dict[str, str]
    emails: Dict[str, str]

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        if not __pydantic_self__.root_dir.exists():
            raise FileNotFoundError(f"Root directory '{__pydantic_self__.__root_dir}' does not exist.")
        if not __pydantic_self__.config_dir.exists():
            raise FileNotFoundError(f"Config directory '{__pydantic_self__.__config_dir}' does not exist.")
        __pydantic_self__.working_dir = __pydantic_self__.root_dir / __pydantic_self__.working_dir
