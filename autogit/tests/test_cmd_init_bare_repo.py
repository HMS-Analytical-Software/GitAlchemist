import os
from pathlib import Path

from autogit import AutoGitTask
from autogit.commands import CMDInitBareRepo

from .conftest import my_config_dir, my_rel_working_dir
from .utils import ConfigBuilder


def test_init_bare_repo(config_builder: ConfigBuilder):
    """Test the init_bare_repo command that is used to boostrap an empty remote repository"""
    config = config_builder.create(task_name="init_bare_repo",
                                   config_dir=my_config_dir,
                                   rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)

    # make sure we have only the init_bare_repo command
    assert len(task.model.commands) == 1
    assert type(task.model.commands[0].get("init_bare_repo")) is CMDInitBareRepo

    # the repo variables should not exist prior to init_bare_repo step
    assert config.bare_dir is None
    assert config.repo_dir is None

    # execute the first and only step
    task.execute_next_step()
    assert task.last_command.cmd_type == "init_bare_repo"
    assert task.next_step_ind == 1

    # check that repos exists
    assert config.bare_dir.exists()
    assert config.repo_dir.exists()

    # verify bare repo
    os.chdir(config.bare_dir)
    assert os.system("git rev-parse --is-bare-repository") == 0

    # verify cloned repo
    os.chdir(config.repo_dir)
    assert Path('.git').exists()
    show_origin = os.popen("git remote show origin").read()
    assert "Fetch URL: ../remotes/init_bare_repo_test" in show_origin
    assert "Push  URL: ../remotes/init_bare_repo_test" in show_origin
