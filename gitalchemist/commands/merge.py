from typing import Literal

from gitalchemist.cmd_base_model import CMDBaseModel
from gitalchemist.config_model import GitAlchemistConfig


class CMDMerge(CMDBaseModel):
    """
    Execute the `git checkout target` command in the git working directory followed
    by a  `git merge source` command.

    Raises:
        GitAlchemistError: raised from cmd.os_system when the git command can not be executed
    """
    cmd_type: Literal['merge']
    source: str
    target: str
    delete_source: bool

    @staticmethod
    def execute(cmd: 'CMDMerge', config: GitAlchemistConfig):
        with cmd.current_repo(config) as (_, _):
            c = f"git checkout {cmd.target}"
            cmd.os_system(c)
            c = f"git merge {cmd.source}"
            cmd.os_system(c)
            if cmd.delete_source:
                c = f"git branch -d {cmd.source}"
                cmd.os_system(c)
