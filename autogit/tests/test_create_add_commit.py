import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest

from autogit.task import AutoGitTask

from .utils import ConfigBuilder, hashfile


my_config_dir = Path("test_configs").resolve()
my_rel_working_dir = Path("cwd", f"{time.time()}")


assert shutil.which("git") is not None, "No git executable found, aborting."


@pytest.fixture
def config_builder(tmp_path):
    return ConfigBuilder(root_dir=tmp_path)


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


def test_create_add_commit_file_contents(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="create_add_commit_track_file_contents", \
                                   config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute()
    os.chdir(config.repo_dir)
    # check that repository is in the intended state: 3 commits should have been run
    assert int(os.popen("git rev-list --count HEAD").read().strip()) == 3
    assert os.path.exists("project_plan.md")
    assert hashfile("project_plan.md") == hashfile(task.config.config_dir / task.config.task / "files" / "project_plan_v3.md")
