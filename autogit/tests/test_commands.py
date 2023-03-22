import os
import subprocess
from pathlib import Path

from autogit.task import AutoGitTask

from .utils import ConfigBuilder
from .conftest import my_config_dir, my_rel_working_dir


def test_init_bare_repo(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="init_bare_repo", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_remaining_steps()
    os.chdir(config.bare_dir)
    # check that bare repository is rare and that it has been cloned successfully
    assert os.system("git rev-parse --is-bare-repository") == 0
    os.chdir(config.repo_dir)
    assert Path('.git').exists()
    result = subprocess.run(['git', 'ls-remote'])
    assert result.returncode == 0
