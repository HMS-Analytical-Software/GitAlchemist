import os

from gitalchemist import GitAlchemistConfig, GitAlchemistTask
from gitalchemist.commands import CMDAdd, CMDCommit, CMDCreateFile, CMDInitBareRepo

from .conftest import my_config_dir, my_rel_working_dir
from .utils import ConfigBuilder


def test_basic_workflow(config_builder: ConfigBuilder):
    """
    Test basic gitalchemist workflow. For this, we verify all steps from a sample
    workflow gitalchemist.yaml file specified in test_configs/basic_workflow. This file
    consists of four steps:

      step1: init_bare_repo in remotes/create_add_commit and clone it to basic_workflow
      step2: create project_plan.md from source files/project_plan_v1.md
      step3: add project_plan.md to index
      step4: commit message with message "Added first file" using author red

    Validation code for these four steps is implemented in separate functions
    for better readibility (this would normally be executed a loop).

    PS: This is also a good example to see how the GitAlchemist commands are executed in
    general. Just follow the execution in this test file step by step.
    """
    config = config_builder.create(task_name="basic_workflow",
                                   config_dir=my_config_dir,
                                   rel_working_dir=my_rel_working_dir)
    task = GitAlchemistTask.parse(config)
    # make sure we have 4 commands in the gitalchemist file as expected
    assert len(task.model.commands) == 4
    # make sure the four commands match the description above
    assert type(task.model.commands[0].get("init_bare_repo")) is CMDInitBareRepo
    assert type(task.model.commands[1].get("create_file")) is CMDCreateFile
    assert type(task.model.commands[2].get("add")) is CMDAdd
    assert type(task.model.commands[3].get("commit")) is CMDCommit
    # execute the commands and check that they are executed as expected;
    # note that each function below calls execute_next_step()
    # on the task object which will "continue" execution inside the task
    _run_and_verify_step_1_init_bare_repo(config, task)
    _run_and_verify_step_2_create_file(config, task)
    _run_and_verify_step_3_git_add(config, task)
    _run_and_verify_step_4_git_commit(config, task)


def _run_and_verify_step_1_init_bare_repo(config: GitAlchemistConfig, task: GitAlchemistTask):
    """verify step 1: make sure that the bare repo is created"""
    # last task
    assert task.last_command is None
    assert task.next_step_ind == 0

    # run command
    task.execute_next_step()
    assert task.last_command.cmd_type == "init_bare_repo"  # this command
    assert task.next_step_ind == 1  # should be one greater than above

    # check command results
    assert config.bare_dir.exists()  # bare repo should exist now
    assert config.bare_dir.is_dir()  # must be a directory
    assert config.bare_dir.stem == "create_add_commit"  # bare repo name we specified in gitalchemist file


def _run_and_verify_step_2_create_file(config: GitAlchemistConfig, task: GitAlchemistTask):
    """verify step 2: make sure that the file project_plan.md exists in the cloned repo"""
    # last task
    assert task.last_command.cmd_type == "init_bare_repo"
    assert task.next_step_ind == 1

    # run command
    task.execute_next_step()
    assert task.last_command.cmd_type == "create_file"  # this command
    assert task.next_step_ind == 2  # should be one greater than above

    # check command results
    os.chdir(config.repo_dir)
    assert os.path.exists("project_plan.md")


def _run_and_verify_step_3_git_add(config: GitAlchemistConfig, task: GitAlchemistTask):
    """verify step 3: make sure that new file is added to the index"""
    # last task
    assert task.last_command.cmd_type == "create_file"
    assert task.next_step_ind == 2

    # run command
    task.execute_next_step()
    assert task.last_command.cmd_type == "add"  # this command
    assert task.next_step_ind == 3  # should be one greater than above

    # make sure the status tracks project_plan.md correctly
    os.chdir(config.repo_dir)
    assert os.popen(
        "git status --short").read().strip() == "A  project_plan.md"


def _run_and_verify_step_4_git_commit(config: GitAlchemistConfig, task: GitAlchemistTask):
    """verify step 4: make sure that the commit command worked as expected"""
    # last task
    assert task.last_command.cmd_type == "add"
    assert task.next_step_ind == 3
    os.chdir(config.repo_dir)

    # prior to the commit, we expect the git status to be as follows:
    # --------------- git status output ---------------
    # On branch main
    # No commits yet
    #
    # Changes to be committed:
    # (use "git rm --cached <file>..." to unstage)
    #         new file:   project_plan.md
    status = os.popen("git status").read()
    assert "On branch main" in status
    assert "No commits yet" in status
    assert "Changes to be committed" in status
    assert "new file:" in status
    assert "project_plan.md" in status

    # run command (=commit the file project_plan.md)
    task.execute_next_step()
    assert task.last_command.cmd_type == "commit"  # this command
    assert task.next_step_ind == 4  # should be one greater than above

    # verify post-commit status via git log; we expect something like:
    # --------------- git log output ---------------
    # Status commit 2e796f81123bfa843f6e2563e1c465ba2fc84367
    # Author: Richard Red <richard@pw-compa.ny>
    # Date:   Thu Apr 20 08:03:15 2023 +0200
    # Added first file
    os.chdir(config.repo_dir)
    log = os.popen("git log").read()
    assert "Author: Richard Red <richard@pw-compa.ny>" in log
    assert "Added first file" in log  # commit message as defined in gitalchemist.yaml
