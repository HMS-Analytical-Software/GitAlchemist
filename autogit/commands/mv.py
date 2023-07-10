from typing import Literal

from gitalchemist.cmd_base_model import CMDBaseModel
from gitalchemist.config_model import GitAlchemistConfig


class CMDMv(CMDBaseModel):
    """
    Execute the `git mv source target` command in the git working directory.

    Raises:
        GitAlchemistError: raised from cmd.os_system when the git command can not be executed
    """
    cmd_type: Literal['mv']
    source: str
    target: str

    @staticmethod
    def execute(cmd: 'CMDMv', config: GitAlchemistConfig):
        with cmd.current_repo(config) as (_, _):
            c = f"git mv {cmd.source} {cmd.target}"
            cmd.os_system(c)
