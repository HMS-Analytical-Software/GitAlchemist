import os
import pytest
from autogit.exceptions import GitCommandError

from autogit.task import AutoGitTask

from .utils import ConfigBuilder
from .conftest import my_config_dir, my_rel_working_dir

# tests if git mv works
def test_git_mv(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="git_branches", \
                                   config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(4)
    os.chdir(config.repo_dir)
    assert os.path.exists("generator.py")
    assert not os.path.exists("main.py")


# test if git push leads to same repository contents as repository that was pushed from
def test_git_push(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="git_branches", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(7)
    os.chdir(config.working_dir)
    # bare_dir is remote_dir, see CMDInitBareRepo
    from_repo = f"remotes/{config.bare_dir.name}"
    to_repo = "test_clone"
    os.system(f"git clone {from_repo} {to_repo}")
    assert os.listdir(config.current_repo) == os.listdir(f"{to_repo}")


def test_git_branch_checkout(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="git_branches", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_remaining_steps()
    os.chdir(config.repo_dir)
    assert int(os.popen("git branch | wc -l").read().strip()) == 2


def test_git_merge(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="git_branches", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_remaining_steps()
    os.chdir(config.repo_dir)
