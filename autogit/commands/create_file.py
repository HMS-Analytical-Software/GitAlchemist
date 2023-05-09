import shutil
import time
from typing import Literal

from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDCreateFile(CMDBaseModel):
    """
    Copy source into target.

    See tests/test_basic_workflow.py and test-configs/basic_workflow
    for examples how to use this.

    Note that we recommend to stick with CMDCreateAddCommit which is easier to
    use and read in the autogit.yaml files. All our newer tasks are build exclusively
    with CMDCreateAddCommit.
    """
    cmd_type: Literal['create_file']
    source: str
    target: str

    @staticmethod
    def execute(cmd: 'CMDCreateFile', config: AutoGitConfig):
        with cmd.current_repo(config) as (repo, task):
            source = task.joinpath(cmd.source)
            target = repo.joinpath(cmd.target)
            cmd._log("cp", source, target)
            shutil.copy(source, target)
            time.sleep(0.5)
