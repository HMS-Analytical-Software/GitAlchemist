import shutil
import time
from typing import Literal

from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDCreateFile(CMDBaseModel):
    cmd_type: Literal['create_file']
    source: str
    target: str

    @staticmethod
    def execute(cmd: 'CMDCreateFile', config: AutoGitConfig):
        with cmd.current_repo(config) as (repo, task):
            source = task.joinpath(cmd.source)
            target = repo.joinpath(cmd.target)
            cmd.log("cp", source, target)
            shutil.copy(source, target)
            time.sleep(0.5)
