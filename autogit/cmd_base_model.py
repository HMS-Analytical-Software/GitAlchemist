import contextlib
import os
import shutil
import time
from collections.abc import Generator
from pathlib import Path
from typing import Tuple

from pydantic import BaseModel

from autogit.config_model import AutoGitConfig
from autogit.exceptions import GitCommandError


class CMDBaseModel(BaseModel):

    def log(self, *msg):
        print("    >", *msg)

    def os_system(self, command: str) -> int:
        self.log(command)
        exit_status = os.system(command)
        if exit_status != 0:
            raise GitCommandError(f"One of the `git` commands failed, exit_status is {exit_status}")
        return exit_status
    
    def switch_dir_and_log(self, target_dir):
        self.log("cd", target_dir)
        os.chdir(target_dir)

    def os_cp(self, source: Path, target: Path):
        self.log("cp", source, target)
        shutil.copy(source, target)
        time.sleep(0.5)

    @contextlib.contextmanager
    def current_repo(self, config: AutoGitConfig) -> Generator[Tuple[Path, Path], None, None]:
        configs_task_dir = config.config_dir / config.task
        assert configs_task_dir.exists()

        try:
            os.chdir(config.repo_dir)
            self.log(f"cd {config.working_dir}")
            yield config.repo_dir, configs_task_dir
        finally:
            self.log(f"cd back to root dir ({config.root_dir})")
            os.chdir(config.root_dir)
