import pytest
import sys
import pdb
import time
import os
from pathlib import Path
from autogit.config_model import AutoGitConfig
from autogit.task import AutoGitTask
import subprocess
from .utils import ConfigBuilder

from .. import config_env

print(f"__name__: {__name__}")
print(f"sys.path: {sys.path}")

my_config_dir = Path("test_configs").resolve()
my_rel_working_dir = Path("cwd", f"{time.time()}")


@pytest.fixture
def config_builder(tmp_path):
    return ConfigBuilder(root_dir=tmp_path)


def test_git_path(git_path=config_env.git_path):
    assert os.path.isfile(git_path)


def test_init_bare_repo(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="init_bare_repo", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute()
    os.chdir(config.bare_dir)
    # check that bare repository is rare and that it has been cloned successfully
    assert os.system("git rev-parse --is-bare-repository") == 0
    os.chdir(config.repo_dir)
    assert Path('.git').exists()
    result = subprocess.run(['git', 'ls-remote'])
    assert result.returncode == 0


def test_create_add_commit(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="create_add_commit", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute()
    os.chdir(config.repo_dir)
    # check that repository is in the intended state
    assert int(os.popen("git rev-list --count HEAD").read().strip()) == 1
    assert os.popen("git log -1 --pretty=%B").read().strip() == "hello world"
    assert os.path.exists("hello.py")
    assert os.path.exists("README.md")


def test_remove_and_commit(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="remove_and_commit", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute()
    assert not os.path.exists("notes-timeline.txt")


def test_git_push(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="git_push", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute()
