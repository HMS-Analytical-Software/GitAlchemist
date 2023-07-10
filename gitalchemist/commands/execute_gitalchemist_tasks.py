from typing import List, Literal
from gitalchemist.cmd_base_model import CMDBaseModel
from gitalchemist.config_model import GitAlchemistConfig


class CMDExecuteGitAlchemistTasks(CMDBaseModel):
    cmd_type: Literal['execute_gitalchemist_tasks']
    skip: bool
    tasks: List[str]

    @staticmethod
    def execute(cmd: 'CMDExecuteGitAlchemistTasks', config: GitAlchemistConfig):

        if cmd.skip:
            # skip running tasks; was added here so that it easy
            # to switch loading old tasks on and off without having
            # to uncomment or remove the entry in the gitalchemist.yaml file
            return

        for task in cmd.tasks:
            cfg = config.dict()
            cfg["task"] = task
            new_config = GitAlchemistConfig(**cfg)

            # we avoid circular import when we import it at runtime
            from gitalchemist.task import GitAlchemistTask
            new_task = GitAlchemistTask.parse(new_config)
            new_task.execute_remaining_steps(skip_commands=["init_bare_repo"])
