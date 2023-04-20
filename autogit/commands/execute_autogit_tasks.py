from typing import List, Literal
from autogit.cmd_base_model import CMDBaseModel
from autogit.config_model import AutoGitConfig


class CMDExecuteAutogitTasks(CMDBaseModel):
    cmd_type: Literal['execute_autogit_tasks']
    skip: bool
    tasks: List[str]

    @staticmethod
    def execute(cmd: 'CMDExecuteAutogitTasks', config: AutoGitConfig):

        if cmd.skip:
            # skip running tasks; was added here so that it easy
            # to switch loading old tasks on and off without having
            # to uncomment or remove the entry in the autogit.yaml file
            return

        for task in cmd.tasks:
            cfg = config.dict()
            cfg["task"] = task
            new_config = AutoGitConfig(**cfg)

            # we avoid circular import when we import it at runtime
            from autogit.task import AutoGitTask
            new_task = AutoGitTask.parse(new_config)
            new_task.execute_remaining_steps(skip_commands=["init_bare_repo"])
