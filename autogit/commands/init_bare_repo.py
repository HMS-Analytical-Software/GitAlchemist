from pathlib import Path
import shutil
import os
from typing import Literal
from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDInitBareRepo(CMDBaseModel):
    cmd_type: Literal['init_bare_repo']
    bare: str
    clone_to: str

    @staticmethod
    def execute(cmd: 'CMDInitBareRepo', config: AutoGitConfig):
        dir_root = Path(config.root_dir)
        assert(dir_root.exists())

        # the current working directly
        dir_cwd = dir_root.joinpath(config.working_dir)
        dir_cwd.mkdir(exist_ok=True, parents=True)

        # create the remote repo
        if not cmd.bare.startswith("remotes/"):
            raise RuntimeWarning("bare parameter of init_bare_repo should always start with remotes/")
        bare_dir = dir_cwd.joinpath(cmd.bare)
        bare_dir.mkdir(exist_ok=False, parents=True)

        # save cwd
        save_cwd = os.getcwd()

        # switch to the bare repository folder
        os.chdir(bare_dir)
        cmd.log("cd", bare_dir)

        # create a new bare git repo by calling the below command
        cmd.os_system("git --bare init .")

        # go back to dir_cwd
        os.chdir(dir_cwd)
        cmd.log("cd", dir_cwd)

        # delete the working repo if it already exists
        repo_dir = dir_cwd.joinpath(cmd.clone_to)
        if repo_dir.exists():
            cmd.log("rm", repo_dir)
            shutil.rmtree(repo_dir)

        # clone the newly created repo into the repo_dir folder
        cmd.os_system(f'git clone {cmd.bare} {cmd.clone_to}')

        # update origin to relative path
        os.chdir(cmd.clone_to)
        cmd.log("cd", cmd.clone_to)
        cmd.os_system(f'git remote set-url origin ../{cmd.bare}')

        # set git config otherwise subsequent commits will fail
        cmd.os_system(f"git config user.name '{config.authors.get('red')}'")
        cmd.os_system(f"git config user.email '{config.emails.get('red')}'")

        # set the current_repo parameter in config file
        config.current_repo = cmd.clone_to
        cmd.log(f"In {__name__}: set config.current_repo to {cmd.clone_to}")

        # go back to original cwd
        os.chdir(save_cwd)
