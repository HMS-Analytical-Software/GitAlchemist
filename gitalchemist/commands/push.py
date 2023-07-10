from typing import Literal

from gitalchemist.cmd_base_model import CMDBaseModel
from gitalchemist.config_model import GitAlchemistConfig


class CMDPush(CMDBaseModel):
    """
    Execute the `git push origin master` command in the git working directory.

    Raises:
        GitAlchemistError: raised from cmd.os_system when the git command can not be executed
    """
    cmd_type: Literal['push']
    master: bool

    @staticmethod
    def execute(cmd: 'CMDPush', config: GitAlchemistConfig):
        with cmd.current_repo(config) as (_, _):
            if cmd.master:
                cmd.os_system("git push origin master")
