from typing import Literal

from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDPush(CMDBaseModel):
    """
    Execute the `git push origin master` command in the git working directory.

    Raises:
        AutogitError: raised from cmd.os_system when the git command can not be executed
    """
    cmd_type: Literal['push']
    master: bool

    @staticmethod
    def execute(cmd: 'CMDPush', config: AutoGitConfig):
        with cmd.current_repo(config) as (_, _):
            if cmd.master:
                cmd.os_system("git push origin master")
