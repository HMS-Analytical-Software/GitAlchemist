import os
import pytest
from autogit.exceptions import GitCommandError

from autogit.task import AutoGitTask

from .utils import ConfigBuilder
from .conftest import my_config_dir, my_rel_working_dir


def test_create_file(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="basic_workflow", \
                                   config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(2)
    assert task.last_command.cmd_type == "create_file"
    os.chdir(config.repo_dir)
    assert os.path.exists("project_plan.md")


def test_git_mv(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="git_branches", \
                                   config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(3)
    assert task.last_command.cmd_type == "mv"
    os.chdir(config.repo_dir)
    assert os.path.exists(task.last_command.target)
    assert not os.path.exists(task.last_command.source)


def test_git_add(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="basic_workflow", \
                                   config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(3)
    assert task.last_command.cmd_type == "add"
    os.chdir(config.repo_dir)
    assert os.popen("git status --short").read().strip() == "A  project_plan.md"
    

def test_git_commit(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="basic_workflow", \
                                   config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(4)
    assert task.last_command.cmd_type == "commit"
    os.chdir(config.repo_dir)
    assert int(os.popen("git status --short | wc -l").read().strip()) == 0
    assert int(os.popen("git rev-list --count HEAD").read().strip()) == 1


def test_remove_and_commit(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="remove_and_commit", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(3)
    assert task.last_command.cmd_type == "remove_and_commit"
    assert not os.path.exists("notes-timeline.txt")


def test_remove_and_commit_fail(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="remove_and_commit", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    with pytest.raises(GitCommandError):
        task.execute_remaining_steps()
