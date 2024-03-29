import contextlib
import logging
import os
import shutil
import shlex
import subprocess
import time
from collections.abc import Generator
from pathlib import Path
from typing import Tuple

from pydantic import BaseModel

from gitalchemist.config_model import GitAlchemistConfig
from gitalchemist.exceptions import GitAlchemistError

logger = logging.getLogger(__name__)


class CMDBaseModel(BaseModel):

    def _log(self, *msg):
        """small wrapper to format the logging info"""
        logger.debug("    > " + " ".join([str(el) for el in msg]))

    def os_system(self, command: str) -> int:
        self._log(command)
        command = command.replace("\\", "\\\\")
        command_split = shlex.split(command)
        if command_split[0] != "git":
            raise GitAlchemistError(f"Only git commands are allowed in the gitalchemist.yaml file. However, the following command was found: '{command_split[0]}'")
        result = subprocess.run(command_split, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if result.returncode != 0:
            raise GitAlchemistError(f"\nONE OF THE `git` COMMANDS FAILED.\n"
                               f"COMMAND: '{command}'\n"
                               f"GIT VERSION: {subprocess.run(['git', '--version'], stdout=subprocess.PIPE).stdout.decode('utf-8')}"
                               f"EXIT_STATUS: {result.returncode}\n"
                               f"STDERR: {result.stderr.decode('utf-8')}\n"
                               f"STDOUT: {result.stdout.decode('utf-8')}")
        return result.returncode

    def switch_dir_and_log(self, target_dir):
        self._log("cd", target_dir)
        os.chdir(target_dir)

    def os_cp(self, source: Path, target: Path):
        self._log("cp", source, target)
        shutil.copy(source, target)
        time.sleep(0.5)

    @contextlib.contextmanager
    def current_repo(self, config: GitAlchemistConfig) -> Generator[Tuple[Path, Path], None, None]:
        configs_task_dir = config.config_dir / config.task
        if not os.path.exists(configs_task_dir):
            raise FileNotFoundError(f"Task directory '{configs_task_dir}' does not exist.")
        try:
            os.chdir(config.repo_dir)
            self._log(f"cd {config.working_dir}")
            yield config.repo_dir, configs_task_dir
        finally:
            self._log(f"cd back to root dir ({config.root_dir})")
            os.chdir(config.root_dir)
