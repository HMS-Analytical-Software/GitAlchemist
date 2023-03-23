import os
import pytest
from autogit.exceptions import GitCommandError

from autogit.task import AutoGitTask

from .utils import ConfigBuilder
from .conftest import my_config_dir, my_rel_working_dir


def test_git_mv(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="git_branches", \
                                   config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(4)
    os.chdir(config.repo_dir)
    assert os.path.exists("generator.py")
    assert not os.path.exists("main.py")


def test_create_file(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="basic_workflow", \
                                   config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)


def test_git_add(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="basic_workflow", \
                                   config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    

def test_git_commit(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="basic_workflow", \
                                   config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)


def test_remove_and_commit(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="remove_and_commit", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(3)
    assert not os.path.exists("notes-timeline.txt")


def test_remove_and_commit_fail(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="remove_and_commit", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    with pytest.raises(GitCommandError):
        task.execute_remaining_steps()
