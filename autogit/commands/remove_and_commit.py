from typing import List, Literal

from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


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
                cmd.os_system(f"git rm {entry}")

            # commit
            author = config.authors.get(cmd.author, cmd.author)
            c = f"git commit --date=\"format:relative:5.hours.ago\" -m \"{cmd.message}\" --author=\"{author}\""
            cmd.os_system(c)
