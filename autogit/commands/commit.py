from typing import Literal

from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDCommit(CMDBaseModel):
    """
    Use git commit in the current repository.

    See tests/test_basic_workflow.py and test-configs/basic_workflow
    for examples how to use this.

    Note that we recommend to stick with CMDCreateAddCommit which is easier to
    use and read in the autogit.yaml files. All our newer tasks are build exclusively
    with CMDCreateAddCommit.
    """
    cmd_type: Literal['commit']
    message: str
    author: str

    @staticmethod
    def execute(cmd: 'CMDCommit', config: AutoGitConfig):
        with cmd.current_repo(config) as (_, _):
            author = config.authors.get(cmd.author, cmd.author)
            c = f"git commit --date=\"format:relative:5.hours.ago\" -m \"{cmd.message}\" --author=\"{author}\""
            cmd.os_system(c)
