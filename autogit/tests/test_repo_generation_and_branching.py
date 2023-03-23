import os
import subprocess

from pathlib import Path
from autogit.task import AutoGitTask

from .utils import ConfigBuilder
from .conftest import my_config_dir, my_rel_working_dir


def test_init_bare_repo(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="init_bare_repo", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_remaining_steps()
    assert task.last_command.cmd_type == "init_bare_repo"
    os.chdir(config.bare_dir)
    # check that repository is bare and that it has been cloned successfully
    assert os.system("git rev-parse --is-bare-repository") == 0
    os.chdir(config.repo_dir)
    assert Path('.git').exists()
    result = subprocess.run(['git', 'ls-remote'])
    assert result.returncode == 0


# test if git push leads to same repository contents as repository that was pushed from
def test_git_push(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="git_branches", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(7)
    assert task.last_command.cmd_type == "git"
    os.chdir(config.working_dir)
    # bare_dir is remote_dir, see CMDInitBareRepo
    from_repo = f"remotes/{config.bare_dir.name}"
    to_repo = "test_clone"
    os.system(f"git clone {from_repo} {to_repo}")
    assert os.listdir(config.current_repo) == os.listdir(f"{to_repo}")


def test_git_branch_checkout(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="git_branches", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(11)
    os.chdir(config.repo_dir)
    assert int(os.popen("git branch | wc -l").read().strip()) == 2


def test_git_merge(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="git_branches", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_remaining_steps()
