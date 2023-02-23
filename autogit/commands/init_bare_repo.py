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
    
    @staticmethod
    def execute(cmd: 'CMDInitBareRepo', config: AutoGitConfig):
        assert(config.root_dir.exists())
        if not cmd.bare.startswith("remotes/"):
            raise RuntimeWarning("bare parameter of init_bare_repo should always start with remotes/")
        
        save_cwd = os.getcwd()
        os.chdir(config.root_dir)
        cmd.log("cd", config.root_dir)

        # We register the paths in the config object (which is shared between calls) 
        # to make things more explicit and make testing of directory contents easier later on
        config.working_dir = config.root_dir / config.working_dir
        config.working_dir.mkdir(exist_ok=True, parents=True)
        config.bare_dir = config.working_dir / cmd.bare
        config.bare_dir.mkdir(exist_ok=True, parents=True)

        # switch to the bare repository folder
        os.chdir(config.bare_dir)
        cmd.log("cd", config.bare_dir)

        # create a new bare git repo by calling the below command
        cmd.os_system("git --bare init .")

        # go back to dir_cwd
        os.chdir(config.working_dir)
        cmd.log("cd", config.working_dir)

        # delete the working repo if it already exists
        config.repo_dir = config.working_dir.joinpath(cmd.clone_to)
        if config.repo_dir.exists():
            cmd.log("rm", cmd.repo_dir)
            shutil.rmtree(config.repo_dir)

        cmd.os_system(f'git clone {cmd.bare} {cmd.clone_to}')

        os.chdir(cmd.clone_to)
        cmd.log("cd", cmd.clone_to)
        pdb.set_trace()
        cmd.os_system(f'git remote set-url origin ../{cmd.bare}')

        # set git config otherwise subsequent commits will fail
        cmd.os_system(f"git config user.name '{config.authors.get('red')}'")
        cmd.os_system(f"git config user.email '{config.emails.get('red')}'")

        # set the current_repo parameter in config file
        config.current_repo = cmd.clone_to
        cmd.log(f"# setting config.current_repo to {cmd.clone_to}")

        # go back to original cwd
        os.chdir(save_cwd)
        cmd.log("cd", save_cwd)
