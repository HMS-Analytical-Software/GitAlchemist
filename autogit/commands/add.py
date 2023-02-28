from typing import List, Literal

from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDAdd(CMDBaseModel):
    cmd_type: Literal['add']
    files: List[str]

    @staticmethod
    def execute(cmd: 'CMDAdd', config: AutoGitConfig):
        with cmd.current_repo(config) as (_, _):
            for f in cmd.files:
                cmd.os_system(f"git add {f}")
            cmd.os_system("git status")
