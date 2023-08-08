import os

from gitalchemist import GitAlchemistTask

from .conftest import my_config_dir, my_rel_working_dir
from .utils import ConfigBuilder


def test_create_file(config_builder: ConfigBuilder):
    """Test the create_file command which adds a new file to the index
    but does NOT directly commit it."""
    config = config_builder.create(task_name="cmd_create_file",
                                   config_dir=my_config_dir,
                                   rel_working_dir=my_rel_working_dir)
    task = GitAlchemistTask.parse(config)

    # execute the first two steps
    task.execute_next_n_steps(2)
    assert task.last_command.cmd_type == "create_file"
    assert task.next_step_ind == 2

    # assert that the file project_plan.md was created
    os.chdir(config.repo_dir)
    assert not os.path.exists("some_other_file.txt")
    assert os.path.exists("project_plan.md")

    # assert project_plan.md is in untracked state, i.e., NOT added
    untracked_files = os.popen("git ls-files . --exclude-standard --others").read().strip()
    assert "project_plan.md" == untracked_files  # only one entry allowed here after adding first file

    # execute second create_file step
    task.execute_next_step()
    assert task.last_command.cmd_type == "create_file"
    assert task.next_step_ind == 3

    # make sure new file is created and we have 2 untracked files now
    os.chdir(config.repo_dir)
    assert os.path.exists("some_other_file.txt")
    untracked_files = os.popen("git ls-files . --exclude-standard --others").read().strip()
    assert "project_plan.md" in untracked_files
    assert "some_other_file.txt" in untracked_files
