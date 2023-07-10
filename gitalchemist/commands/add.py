from typing import List, Literal

from gitalchemist.cmd_base_model import CMDBaseModel
from gitalchemist.config_model import GitAlchemistConfig


class CMDAdd(CMDBaseModel):
    """
    Use git add in the current repository with a list of files. Requires
    that the requested file is in the current repository which usually means that
    is was created first with create_file. Unlike CMDCreateAddCommit, this
    command will NOT automatically commit the added file.

    See tests/test_basic_workflow.py and test-configs/basic_workflow
    for examples how to use this.

    Note that we recommend to stick with CMDCreateAddCommit which is easier to
    use and read in the gitalchemist.yaml files. All our newer tasks are build exclusively
    with CMDCreateAddCommit.
    """
    cmd_type: Literal['add']
    files: List[str]

    @staticmethod
    def execute(cmd: 'CMDAdd', config: GitAlchemistConfig):
        with cmd.current_repo(config) as (_, _):
            for f in cmd.files:
                cmd.os_system(f"git add {f}")
            cmd.os_system("git status")
