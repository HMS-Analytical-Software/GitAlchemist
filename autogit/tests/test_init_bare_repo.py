import pytest
import sys
import pdb
from pathlib import Path
from autogit.config_model import AutoGitConfig
from autogit.task import AutoGitTask

from .. import config_env

print(f"__name__: {__name__}")
print(f"sys.path: {sys.path}")

# def test_git_path(git_path=config_env.git_path):
#     assert os.path.isfile(git_path)


my_task = "task0"
my_config_dir = Path("test_configs").resolve()

@pytest.fixture
def my_config(tmp_path):
    config = AutoGitConfig(
        task=my_task,
        root_dir=tmp_path, 
        config_dir=my_config_dir, 
        #working_dir=tmp_path,
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


def test_init_bare_repo(my_config):
    task = AutoGitTask.parse(my_config)
    task.execute()

