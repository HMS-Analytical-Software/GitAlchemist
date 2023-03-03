import os
import shutil
from typing import Literal

from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDInitBareRepo(CMDBaseModel):
    cmd_type: Literal['init_bare_repo']
    bare: str
    clone_to: str
    
    @staticmethod
    def execute(cmd: 'CMDInitBareRepo', config: AutoGitConfig):
        if not cmd.bare.startswith("remotes/"):
            raise RuntimeError("bare parameter of init_bare_repo should always start with remotes/")
        
        save_cwd = os.getcwd()
        cmd.switch_dir_and_log(config.root_dir)

        # Register paths that depend on command execution settings during execution 
        # in the config object, which is shared between calls. 
        config.working_dir.mkdir(exist_ok=True, parents=True)
        config.bare_dir = config.working_dir / cmd.bare
        config.bare_dir.mkdir(exist_ok=True, parents=True)

        # switch to the bare repository folder and create a new bare git repo
        cmd.switch_dir_and_log(config.bare_dir)
        cmd.os_system("git --bare init .")

        cmd.switch_dir_and_log(config.working_dir)

        # delete the working repo if it already exists, config.repo_dir is later needed by 
        # the context manager of the CMDBaseModel
        config.repo_dir = config.working_dir / cmd.clone_to
        if config.repo_dir.exists():
            cmd.log("rm", cmd.repo_dir)
            shutil.rmtree(config.repo_dir)

        cmd.os_system(f'git clone {cmd.bare} {cmd.clone_to}')

        cmd.switch_dir_and_log(cmd.clone_to)
        cmd.os_system(f'git remote set-url origin ../{cmd.bare}')

        # set git config otherwise subsequent commits will fail
        cmd.os_system(f"git config user.name \"{config.authors.get('red')}\"")
        cmd.os_system(f"git config user.email \"{config.emails.get('red')}\"")

        # set the current_repo parameter in config file
        config.current_repo = cmd.clone_to
        cmd.log(f"# setting config.current_repo to {cmd.clone_to}")

        # go back to original cwd
        cmd.switch_dir_and_log(save_cwd)
