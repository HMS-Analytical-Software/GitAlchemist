import os
import pytest
from autogit.exceptions import GitCommandError

from autogit.task import AutoGitTask

from .utils import ConfigBuilder
from .conftest import my_config_dir, my_rel_working_dir


def test_remove_and_commit(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="remove_and_commit", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_remaining_steps()
    assert not os.path.exists("notes-timeline.txt")

def test_remove_and_commit_fail(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="remove_and_commit_fail", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    with pytest.raises(GitCommandError):
        task.execute_remaining_steps()
