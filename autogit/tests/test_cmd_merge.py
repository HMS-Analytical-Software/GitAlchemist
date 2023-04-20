import os

from autogit import AutoGitTask
from autogit.commands import (CMDCreateAddCommit, CMDGit, CMDInitBareRepo,
                              CMDMerge, CMDPush)

from .conftest import my_config_dir, my_rel_working_dir
from .utils import ConfigBuilder


def test_cmd_merge(config_builder: ConfigBuilder):
    """
    Test checkout and merge command with autogit. For this we use the autogit.yaml file specified
    in test_configs/cmd_merge which consists of the following steps:

      step1: init_bare_repo
      step2: create_add_commit (readme.md)
      step3: push master
      step4: checkout new feature branch
      step5: create_add_commit (main.py, .gitignore)
      step6: push feature branch
      step7: merge
      step8: push master
    """
    config = config_builder.create(task_name="cmd_merge",
                                   config_dir=my_config_dir,
                                   rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)

    # make sure we have the correct config file
    assert type(task.model.commands[0].get("init_bare_repo")) is CMDInitBareRepo
    assert type(task.model.commands[1].get("create_add_commit")) is CMDCreateAddCommit
    assert type(task.model.commands[2].get("push")) is CMDPush
    assert type(task.model.commands[3].get("git")) is CMDGit
    assert type(task.model.commands[4].get("create_add_commit")) is CMDCreateAddCommit
    assert type(task.model.commands[5].get("git")) is CMDGit
    assert type(task.model.commands[6].get("merge")) is CMDMerge
    assert type(task.model.commands[7].get("push")) is CMDPush

    # run the first three steps that will create a readme file, add, commit and
    # push to master
    task.execute_next_n_steps(3)
    assert task.last_command.cmd_type == "push"
    assert task.next_step_ind == 3

    # we expect that git status says that we are on master then
    os.chdir(config.repo_dir)
    status = os.popen("git status").read()
    assert "On branch master" in status
    assert "branch is up to date" in status

    # run the checkout command
    task.execute_next_step()
    assert task.last_command.cmd_type == "git"
    assert task.next_step_ind == 4

    # we expect that git status says we are on the checked out feature branch now
    os.chdir(config.repo_dir)
    status = os.popen("git status").read()
    assert "On branch feature/start_project" in status

    # run the next two commands where we add data to the feature branch and
    # merge the changes back to master (but not pushing yet)
    task.execute_next_n_steps(3)
    assert task.last_command.cmd_type == "merge"
    assert task.next_step_ind == 7

    # we expect that we are now ahead of origin/master by one commit
    os.chdir(config.repo_dir)
    status = os.popen("git status").read()
    assert "Your branch is ahead of 'origin/master' by 1 commit" in status
