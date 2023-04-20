import os

from autogit import AutoGitTask

from .utils import ConfigBuilder, hashfile
from .conftest import my_config_dir, my_rel_working_dir


def test_create_add_commit(config_builder: ConfigBuilder):
    """Test the create_add_commit command which adds a new file to the index
    and directly commits it. This test uses the same autogit.yaml file as the
    test below (see comments there for further details)."""
    config = config_builder.create(task_name="cmd_create_add_commit",
                                   config_dir=my_config_dir,
                                   rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)

    # execute the first two steps
    task.execute_next_n_steps(2)
    assert task.last_command.cmd_type == "create_add_commit"
    assert task.next_step_ind == 2

    # check that repository is in the intended state
    os.chdir(config.repo_dir)
    assert int(os.popen("git rev-list --count HEAD").read().strip()) == 1
    assert os.popen(
        "git log -1 --pretty=%B").read().strip() == "added project plan template"
    assert os.path.exists("project_plan.md")


def test_create_add_commit_multiple_uses(config_builder: ConfigBuilder):
    """
    It is common that the same file is overwritten multiple
    times using multiple create_add_commit commands with different
    source files but same target file. In the example autogit.yaml file
    used for this test (test_configs/create_add_commit) the project_plan.md file
    is updated three times with different contents and commit messages.

      step1: init_bare_repo
      step2: create_add_commit (files/project_plan_v1.md => project_plan.md)
      step3: create_add_commit (files/project_plan_v2.md => project_plan.md)
      step4: create_add_commit (files/project_plan_v3.md => project_plan.md)
      step5: git push

    Note that step5 is not relevant here (i.e., not used) but included in the
    yaml file to give a better understanding of the structure/logic in the file.
    """
    config = config_builder.create(task_name="cmd_create_add_commit",
                                   config_dir=my_config_dir,
                                   rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)

    # execute the first three steps
    task.execute_next_n_steps(3)
    assert task.last_command.cmd_type == "create_add_commit"
    assert task.next_step_ind == 3

    # check that repository is in the intended state: 2 commits should have been run (init_bare_repo doesn't count)
    # and the file content in project_plan.md must be updated to the content from project_plan_v2.md
    os.chdir(config.repo_dir)
    assert int(os.popen("git rev-list --count HEAD").read().strip()) == 2
    assert os.path.exists("project_plan.md")
    assert hashfile("project_plan.md") == hashfile(
        task.config.config_dir / task.config.task / "files" / "project_plan_v2.md")

    # execute the fourth step
    task.execute_next_step()
    assert task.last_command.cmd_type == "create_add_commit"
    assert task.next_step_ind == 4

    # content must now match content on project_plan_v3.md
    os.chdir(config.repo_dir)
    assert os.path.exists("project_plan.md")
    assert hashfile("project_plan.md") == hashfile(
        task.config.config_dir / task.config.task / "files" / "project_plan_v3.md")
