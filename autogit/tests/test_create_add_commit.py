import os

from autogit.task import AutoGitTask

from .utils import ConfigBuilder, hashfile
from .conftest import my_config_dir, my_rel_working_dir


def test_create_add_commit(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="create_add_commit", config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(2)
    assert task.last_command.cmd_type == "create_add_commit"
    os.chdir(config.repo_dir)
    # check that repository is in the intended state
    assert int(os.popen("git rev-list --count HEAD").read().strip()) == 1
    assert os.popen("git log -1 --pretty=%B").read().strip() == "added project plan template"
    assert os.path.exists("project_plan.md")


def test_create_add_commit_file_contents(config_builder: ConfigBuilder):
    config = config_builder.create(task_name="create_add_commit", \
                                   config_dir=my_config_dir, rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)
    task.execute_next_n_steps(3)
    assert task.last_command.cmd_type == "create_add_commit"
    os.chdir(config.repo_dir)
    # check that repository is in the intended state: 2 commits should have been run (init_bare_repo doesn't count)
    assert int(os.popen("git rev-list --count HEAD").read().strip()) == 2
    assert os.path.exists("project_plan.md")
    assert hashfile("project_plan.md") == hashfile(task.config.config_dir / task.config.task / "files" / "project_plan_v2.md")

    task.execute_next_step()
    assert task.last_command.cmd_type == "create_add_commit"
    os.chdir(config.repo_dir)
    assert os.path.exists("project_plan.md")
    assert hashfile("project_plan.md") == hashfile(task.config.config_dir / task.config.task / "files" / "project_plan_v3.md")
    
