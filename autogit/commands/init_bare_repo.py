from pathlib import Path
import shutil
import os
from typing import Literal
from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig
from autogit.exceptions import GitCommandError
import pdb


class CMDInitBareRepo(CMDBaseModel):
    cmd_type: Literal['init_bare_repo']
    bare: str
    clone_to: str
    root_dir: Path = None
    working_dir: Path = None
    bare_dir: Path = None
    repo_dir: Path = None

    @staticmethod
    def execute(cmd: 'CMDInitBareRepo', config: AutoGitConfig):
        assert(config.root_dir.exists())
        if not cmd.bare.startswith("remotes/"):
            raise RuntimeWarning("bare parameter of init_bare_repo should always start with remotes/")
        
        save_cwd = os.getcwd()

        cmd.root_dir = Path(config.root_dir)
        cmd.working_dir = cmd.root_dir.joinpath(config.working_dir)
        cmd.working_dir.mkdir(exist_ok=True, parents=True)
        cmd.bare_dir = cmd.working_dir.joinpath(cmd.bare)
        cmd.bare_dir.mkdir(exist_ok=True, parents=True)

        # switch to the bare repository folder
        os.chdir(cmd.bare_dir)
        cmd.log("cd", cmd.bare_dir)

        # create a new bare git repo by calling the below command
        cmd.os_system("git --bare init .")

        # go back to dir_cwd
        os.chdir(cmd.working_dir)
        cmd.log("cd", cmd.working_dir)

        # delete the working repo if it already exists
        cmd.repo_dir = cmd.working_dir.joinpath(cmd.clone_to)
        if cmd.repo_dir.exists():
            cmd.log("rm", cmd.repo_dir)
            shutil.rmtree(cmd.repo_dir)

        ## TO DO: cmd.bare and cmd.clone_to are currently relative paths
        ## this is in some way redundant with cmd.bare_dir and cmd.repo_dir so may want to 
        ## convert this to absolute paths but need to check dependency of config.current_repo below first
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
        cmd.log(f"# In {__name__}: set config.current_repo to {cmd.clone_to}")

        # go back to original cwd
        os.chdir(save_cwd)
        cmd.log("cd", save_cwd)
