from typing import Literal

from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDGit(CMDBaseModel):
    """
    Execute a raw git command such as `git status` or `git log` in the
    git working directory. Must be used for functions where no wrapper is available
    such as checkout. Could also be used for some of the functions where a wrapper
    is available such as push or merge.

    There is no real downside of using this generic command
    against the wrapped commands. The commands with file operations such as
    create_add_commit are a noticable difference here because they need to transfer
    files from config directory to the git working directory which is cumbersome
    without a wrapper.

    Raises:
        AutogitError: raised from cmd.os_system when the git command can not be executed
    """
    cmd_type: Literal['git']
    command: str

    @staticmethod
    def execute(cmd: 'CMDGit', config: AutoGitConfig):
        with cmd.current_repo(config) as (_, _):
            cmd.os_system(cmd.command)
