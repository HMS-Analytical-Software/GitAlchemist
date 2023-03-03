import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest

from autogit.task import AutoGitTask

from .utils import ConfigBuilder


my_config_dir = Path("test_configs").resolve()
my_rel_working_dir = Path("cwd", f"{time.time()}")


assert shutil.which("git") is not None, "No git executable found, aborting."


@pytest.fixture
def config_builder(tmp_path):
    return ConfigBuilder(root_dir=tmp_path)


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
    os.chdir(config.working_dir)
    # bare_dir is remote_dir, see CMDInitBareRepo
    from_repo = f"remotes/{config.bare_dir.name}"
    to_repo = "test_clone"
    os.system(f"git clone {from_repo} {to_repo}")
    assert os.listdir(config.current_repo) == os.listdir(f"{to_repo}")
    import pdb; pdb.set_trace()
