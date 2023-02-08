import shutil
import time
from typing import Literal, List
from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDCreateAddCommit(CMDBaseModel):
    cmd_type: Literal['create_add_commit']
    files: List[str] = []
    source: str = None
    target: str = None
    message: str
    author: str

    @staticmethod
    def execute(cmd: 'CMDCreateAddCommit', config: AutoGitConfig):
        with cmd.current_repo(config) as (repo, task):

            if len(cmd.files) == 0:
                cmd.files = [f"{cmd.source} => {cmd.target}"]
                #raise RuntimeError("create_add_commit cannot be used with empty files parameter")
            
            for entry in cmd.files:
                splitted = entry.split("=>")
                if len(splitted) != 2:
                    raise RuntimeError("each entry in create_add_commit.files must be of form \"val1 => val2\"")

                # create
                source = task.joinpath(splitted[0].strip())
                target = repo.joinpath(splitted[1].strip())

                # copy source to target
                cmd.os_cp(source, target)

                # add
                cmd.os_system(f"git add {target}")

            # commit
            author = config.authors.get(cmd.author, cmd.author)
            c = f"git commit --date=\"format:relative:5.hours.ago\" -m \"{cmd.message}\" --author=\"{author}\""
            cmd.os_system(c)
