from typing import List, Literal

from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig
from autogit.exceptions import GitCommandError


class CMDRemoveAndCommit(CMDBaseModel):
    cmd_type: Literal['remove_and_commit']
    files: List[str] = []
    message: str
    author: str

    @staticmethod
    def execute(cmd: 'CMDRemoveAndCommit', config: AutoGitConfig):
        with cmd.current_repo(config) as (repo, task):

            if len(cmd.files) == 0:
                raise RuntimeError("remove_and_commit cannot be used with empty files parameter")
            
            for entry in cmd.files:
                try:
                    cmd.os_system(f"git rm {entry}")
                except GitCommandError as e:
                    print(cmd)
                    raise e

            # commit
            author = config.authors.get(cmd.author, cmd.author)
            c = f"git commit --date=\"format:relative:5.hours.ago\" -m \"{cmd.message}\" --author=\"{author}\""
            try:
                cmd.os_system(c)
            except GitCommandError as e:
                raise e
