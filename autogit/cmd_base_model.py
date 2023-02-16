import contextlib
import os
from pathlib import Path
import shutil
import time
from typing import Tuple
from pydantic import BaseModel
from autogit.config_model import AutoGitConfig
from collections.abc import Generator


class CMDBaseModel(BaseModel):

    def log(self, *msg):
        print("    >", *msg)

    def os_system(self, command: str) -> int:
        self.log(command)
        return os.system(command)

    def os_cp(self, source: Path, target: Path):
        self.log("cp", source, target)
        shutil.copy(source, target)
        time.sleep(0.5)

    @contextlib.contextmanager
    def current_repo(self, config: AutoGitConfig) -> Generator[Tuple[Path, Path], None, None]:
        dir_root = config.root_dir
        assert (dir_root.exists())

        #configs_dir = dir_root.joinpath("configs")
        assert (config.config_dir.exists())

        configs_task_dir = config.config_dir / config.task
        assert (configs_task_dir.exists())

        try:
            #import pdb; pdb.set_trace()
            #repo_dir = dir_root.joinpath(config.working_dir).joinpath(config.current_repo)
            repo_dir = config.root_dir / config.current_repo
            assert (repo_dir.exists)
            os.chdir(repo_dir)
            #self.log(f"cd {config.working_dir}")
            #os.chdir(config.working_dir)
            yield repo_dir, configs_task_dir
        finally:
            self.log(f"cd back to root dir ({dir_root})")
            os.chdir(dir_root)
