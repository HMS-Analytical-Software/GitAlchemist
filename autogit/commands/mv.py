from typing import Literal
from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDMv(CMDBaseModel):
    cmd_type: Literal['mv']
    source: str
    target: str

    @staticmethod
    def execute(cmd: 'CMDMv', config: AutoGitConfig):
        with cmd.current_repo(config) as (_, _):
            c = f"git mv {cmd.source} {cmd.target}"
            cmd.os_system(c)