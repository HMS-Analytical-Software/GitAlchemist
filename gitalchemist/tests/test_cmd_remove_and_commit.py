import pytest

from gitalchemist import GitAlchemistTask
from gitalchemist.commands import (CMDCreateAddCommit, CMDInitBareRepo,
                              CMDRemoveAndCommit)

from .conftest import my_config_dir, my_rel_working_dir
from .utils import ConfigBuilder


def test_remove_and_commit(config_builder: ConfigBuilder):
    """Test the remove_and_commit command which is used to remove files from the index"""
    config = config_builder.create(task_name="cmd_remove_and_commit",
                                   config_dir=my_config_dir,
                                   rel_working_dir=my_rel_working_dir)
    task = GitAlchemistTask.parse(config)

    # for this test we execute four steps in test_configs/cmd_remove_and_commit;
    # the second command will add and commit two files; in step
    # three one of the files should be removed. Step 4 tries to use the command with a file
    # that does not exist which should result in an error
    assert (type(task.model.commands[0].get("init_bare_repo")) is CMDInitBareRepo)
    assert (type(task.model.commands[1].get("create_add_commit")) is CMDCreateAddCommit)
    assert (type(task.model.commands[2].get("remove_and_commit")) is CMDRemoveAndCommit)
    assert (type(task.model.commands[3].get("remove_and_commit")) is CMDRemoveAndCommit)

    # run until step 2 and make sure the file we want to remove exists
    task.execute_next_n_steps(2)
    assert task.last_command.cmd_type == "create_add_commit"
    assert task.next_step_ind == 2
    file_not_to_remove = config.repo_dir.joinpath("hello.py")  # another file created in create_add_commit step
    file_to_remove = config.repo_dir.joinpath("notes-timeline.txt")
    assert file_not_to_remove.exists()
    assert file_to_remove.exists()

    # run step 3 which should work ok
    task.execute_next_step()
    assert task.last_command.cmd_type == "remove_and_commit"
    assert task.next_step_ind == 3
    assert not file_to_remove.exists()  # this must be gone
    assert file_not_to_remove.exists()  # should still exist

    # the next step should fail because the file does not exist
    with pytest.raises(FileNotFoundError):
        task.execute_next_step()
