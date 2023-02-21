import pytest
import sys
import pdb
import time
import os
from pathlib import Path
from autogit.config_model import AutoGitConfig
from autogit.task import AutoGitTask

from .. import config_env

print(f"__name__: {__name__}")
print(f"sys.path: {sys.path}")

my_config_dir = Path("test_configs").resolve()
my_working_dir = os.path.join("cwd", "cwd", f"{time.time()}")

class ConfigBuilder:
    def __init__(self, root_dir, config_dir=my_config_dir, working_dir=my_working_dir):
        self.root_dir = root_dir
        self.config_dir = config_dir
        self.working_dir = working_dir

    def create(self, task_name):
        config = AutoGitConfig(
            task=task_name,
            root_dir=self.root_dir,
            config_dir=self.config_dir,
            working_dir=self.working_dir, 
            authors={
                'red': 'Richard Red <richard@pw-compa.ny>',
                'blue': 'Betty Blue <betty@pw-compa.ny>',
                'green': 'Garry Green <garry@pw-compa.ny>',
            },
            emails={
                'red': 'richard@pw-compa.ny',
                'blue': 'betty@pw-compa.ny',
                'green': 'garry@pw-compa.ny',
            }
        )
        return config


@pytest.fixture
def config_builder(tmp_path):
    return ConfigBuilder(root_dir=tmp_path)


def test_git_path(git_path=config_env.git_path):
    assert os.path.isfile(git_path)


def test_init_bare_repo(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="init_bare_repo")
    task = AutoGitTask.parse(config)
    task.execute()


def test_create_add_commit(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="create_add_commit")
    task = AutoGitTask.parse(config)
    pdb.set_trace()
    task.execute()

