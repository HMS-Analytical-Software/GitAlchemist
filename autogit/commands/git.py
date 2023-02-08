from typing import Literal
from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDGit(CMDBaseModel):
    cmd_type: Literal['git']
    command: str

    @staticmethod
    def execute(cmd: 'CMDGit', config: AutoGitConfig):
        with cmd.current_repo(config) as (_, _):
            cmd.os_system(cmd.command)
