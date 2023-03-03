from typing import Literal
from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDMerge(CMDBaseModel):
    cmd_type: Literal['merge']
    source: str
    target: str
    delete_source: bool

    @staticmethod
    def execute(cmd: 'CMDMerge', config: AutoGitConfig):
        with cmd.current_repo(config) as (_, _):
            c = f"git checkout {cmd.target}"
            cmd.os_system(c)
            c = f"git merge {cmd.source}"
            cmd.os_system(c)
            if cmd.delete_source:
                c = f"git branch -d {cmd.source}"
                cmd.os_system(c)