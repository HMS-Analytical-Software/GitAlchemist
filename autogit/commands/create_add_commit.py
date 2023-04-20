import os.path
from typing import List, Literal

from autogit import AutoGitConfig, AutogitError, CMDBaseModel


class CMDCreateAddCommit(CMDBaseModel):
    """
    This command combines the functionality of add, create_file and commit in
    one command. The files are specified in a special syntax of the form
    source => target where source is a directory in the config directory of the
    task and target is the envisioned name in the git working directory that was
    created within the task. This is the recommended way to build tasks.

    Example usage from task0: The create_add_commit block is specified in the
    autogit.yaml file as follows:

        ```
        create_add_commit:
            files:
                - files/hello.py => hello.py
                - files/README.md => README.md
            message: hello world
            author: red
        ```

    The command expect that two files exist in the config directory of task0, i.e.
    files/hello.py and files/README.md. The command takes these two files and
    copies them to the working directory. The name on the left side of the =>
    operator can be different which is important when you want to overwrite the same
    file twice (i.e., the right part would have the same name).

    After the files are copied to the working directory, a commit operation is
    executed using `message` as commit message and `author` as author.

    Raises:
        AutogitError: raised when the entries in files are not formatted correctly
        FileNotFoundError: raised when a file can not be found
    """
    cmd_type: Literal['create_add_commit']
    files: List[str] = []
    source: str = None
    target: str = None
    message: str
    author: str

    @staticmethod
    def execute(cmd: 'CMDCreateAddCommit', config: AutoGitConfig):
        with cmd.current_repo(config) as (repo, task):

            # optional support for using source and target instead of files; not recommended
            if len(cmd.files) == 0:
                cmd.files = [f"{cmd.source} => {cmd.target}"]

            # run through files and copy them to working directory
            for entry in cmd.files:
                splitted = entry.split("=>")
                if len(splitted) != 2:
                    raise AutogitError("Each entry in create_add_commit.files must be of form \"val1 => val2\"")

                # create
                source = config.root_dir / task.joinpath(splitted[0].strip())
                if not os.path.isfile(source):
                    raise FileNotFoundError(
                        f"Source file {source} in 'create_add_commit' not found. \
                            Please check your autogit config file.")
                target = repo.joinpath(splitted[1].strip())

                # copy source to target
                cmd.os_cp(source, target)

                # add
                cmd.os_system(f"git add {target}")

            # commit
            author = config.authors.get(cmd.author, cmd.author)
            c = f"git commit --date=\"format:relative:5.hours.ago\" -m \"{cmd.message}\" --author=\"{author}\""
            cmd.os_system(c)
