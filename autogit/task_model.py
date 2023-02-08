from typing import Dict, List, Union
from pydantic import BaseModel, Field, validator
from typing_extensions import Annotated
from autogit.commands.add import CMDAdd
from autogit.commands.commit import CMDCommit
from autogit.commands.create_add_commit import CMDCreateAddCommit
from autogit.commands.create_file import CMDCreateFile
from autogit.commands.execute_autogit_tasks import CMDExecuteAutogitTasks
from autogit.commands.git import CMDGit
from autogit.commands.init_bare_repo import CMDInitBareRepo
from autogit.commands.merge import CMDMerge
from autogit.commands.mv import CMDMv
from autogit.commands.push import CMDPush
from autogit.commands.remove_and_commit import CMDRemoveAndCommit


BaseCommand = Annotated[
    Union[
        CMDInitBareRepo,
        CMDCreateFile,
        CMDAdd,
        CMDCommit,
        CMDMv,
        CMDMerge,
        CMDPush,
        CMDGit,
        CMDCreateAddCommit,
        CMDExecuteAutogitTasks,
        CMDRemoveAndCommit
    ],
    Field(discriminator="cmd_type")
]


class AutoGitTaskModel(BaseModel):
    title: str
    commands: List[Dict[str, BaseCommand]]

    # we use a pre-validator to set the cmd_type discriminator
    # based on the dict key because this allows for a much cleaner
    # yaml file
    @validator('commands', pre=True, allow_reuse=True)
    def validate_commands(cls, commands):
        new_list = []
        for cmd in commands:
            new_dict = cmd.copy()
            for k, v in cmd.items():
                new_child = v.copy()
                new_child["cmd_type"] = k
                new_dict[k] = new_child
            new_list.append(new_dict)
        return new_list