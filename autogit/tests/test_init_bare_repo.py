import pytest
import sys
import os
import pdb
from autogit.config_model import AutoGitConfig

from .. import config_env

print(f"__name__: {__name__}")
print(f"sys.path: {sys.path}")


my_task = "task0"

def test_git_path(git_path=config_env.git_path):
    assert os.path.isfile(git_path)


@pytest.fixture
def my_config(tmp_path):
    config = AutoGitConfig(
        root_dir=os.getcwd(),
        working_dir=tmp_path,
        task=my_task,
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
    assert 1 == 1

