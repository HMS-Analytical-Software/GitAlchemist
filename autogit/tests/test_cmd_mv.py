from pathlib import Path

from autogit import AutoGitTask
from autogit.commands import CMDCreateAddCommit, CMDInitBareRepo, CMDMv

from .conftest import my_config_dir, my_rel_working_dir
from .utils import ConfigBuilder


def test_git_mv(config_builder: ConfigBuilder):
    """Test the git mv command which can be used, for example, to rename files"""
    config = config_builder.create(task_name="cmd_mv",
                                   config_dir=my_config_dir,
                                   rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)

    # for this test we execute the autogit yaml file in test_configs/cmd_mv;
    # the second command will add and commit several files, one of which is a main.py file; in step
    # three this file should be renamed to generator.py
    assert (type(task.model.commands[0].get("init_bare_repo")) is CMDInitBareRepo)
    assert (type(task.model.commands[1].get("create_add_commit")) is CMDCreateAddCommit)
    assert (type(task.model.commands[2].get("mv")) is CMDMv)

    # execute the first two commands
    task.execute_next_n_steps(2)
    assert task.last_command.cmd_type == "create_add_commit"
    assert task.next_step_ind == 2

    # we should now have a main.py file
    mainfile = Path(config.repo_dir.joinpath("main.py"))
    mainfile_content = mainfile.read_text()
    assert mainfile.exists()
    assert len(mainfile_content) > 0

    # now execute the third command
    task.execute_next_step()
    assert task.last_command.cmd_type == "mv"
    assert task.next_step_ind == 3

    # check that the mv command was executed as expected
    generatorfile = Path(config.repo_dir.joinpath("generator.py"))
    assert not mainfile.exists()
    assert generatorfile.exists()
    assert generatorfile.read_text() == mainfile_content
