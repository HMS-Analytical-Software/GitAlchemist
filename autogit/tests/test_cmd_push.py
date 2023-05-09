import os

from autogit import AutoGitTask
from autogit.commands import CMDCreateAddCommit, CMDInitBareRepo, CMDPush

from .conftest import my_config_dir, my_rel_working_dir
from .utils import ConfigBuilder


def test_cmd_push(config_builder: ConfigBuilder):
    """
    Test push command. For this we use the autogit.yaml file specified
    in test_configs/cmd_push which consists of three steps:

      step1: init_bare_repo
      step2: create_add_commit (main.py, readme.md, .gitignore)
      step3: push

    We run this and make sure we can clone from the remote repo after
    push was executed.
    """
    config = config_builder.create(task_name="cmd_push",
                                   config_dir=my_config_dir,
                                   rel_working_dir=my_rel_working_dir)
    task = AutoGitTask.parse(config)

    # make sure we have the correct config file
    assert len(task.model.commands) == 3
    assert type(task.model.commands[0].get("init_bare_repo")) is CMDInitBareRepo
    assert type(task.model.commands[1].get("create_add_commit")) is CMDCreateAddCommit
    assert type(task.model.commands[2].get("push")) is CMDPush

    # execute all steps
    task.execute_remaining_steps()
    assert task.last_command.cmd_type == "push"
    assert task.next_step_ind == 3

    # make sure the three files from step 2 exist
    assert config.repo_dir.joinpath("main.py").exists()
    assert config.repo_dir.joinpath("readme.md").exists()
    assert config.repo_dir.joinpath(".gitignore").exists()

    # after pushing (step 3) we expect that the changes made to the repo can
    # be cloned from the remote repository into a new repository that is
    # DIFFERENT from the repo_dir! we verify this here by creating a second
    # repository using the clone command
    os.chdir(config.working_dir)  # note that this is the parent repo!!
    from_repo = f"remotes/{config.bare_dir.name}"  # bare_dir is remote_dir, see CMDInitBareRepo
    to_repo = "test_clone"
    os.system(f"git clone {from_repo} {to_repo}")
    assert config.working_dir.joinpath("test_clone/main.py").exists()
    assert config.working_dir.joinpath("test_clone/readme.md").exists()
    assert config.working_dir.joinpath("test_clone/.gitignore").exists()
    assert os.listdir(config.current_repo) == os.listdir(f"{to_repo}")  # basically same as above
