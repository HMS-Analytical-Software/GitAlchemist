from typing import List, Literal

from autogit import AutoGitConfig, AutogitError, CMDBaseModel


class CMDRemoveAndCommit(CMDBaseModel):
    """
    Removes a file from the git working directory and calls `git rm` followed
    by `git commit`.

    Raises:
        AutogitError: raised from cmd.os_system when the git command can not be executed
        FileNotFoundError: raised when one ore more of the to-be-removed files can not be found
    """
    cmd_type: Literal['remove_and_commit']
    files: List[str] = []
    message: str
    author: str

    @staticmethod
    def execute(cmd: 'CMDRemoveAndCommit', config: AutoGitConfig):
        with cmd.current_repo(config) as (repo, _):

            if len(cmd.files) == 0:
                raise AutogitError("remove_and_commit cannot be used with empty files parameter")

            # make sure the files exist in the git working directory (=repo parameter)
            missing_files = []
            for entry in cmd.files:
                if not repo.joinpath(entry).exists():
                    missing_files.append(entry)
            if len(missing_files) > 0:
                raise FileNotFoundError(f"The following files were not found in git working directory: {missing_files}")

            # call git rm an each file
            for entry in cmd.files:
                cmd.os_system(f"git rm {entry}")

            # commit changes
            author = config.authors.get(cmd.author, cmd.author)
            c = f"git commit --date=\"format:relative:5.hours.ago\" -m \"{cmd.message}\" --author=\"{author}\""
            cmd.os_system(c)
