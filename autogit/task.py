import logging
from pathlib import Path
from typing import List

import yaml

from gitalchemist.config_model import GitAlchemistConfig
from gitalchemist.task_model import GitAlchemistTaskModel

logger = logging.getLogger(__name__)


class GitAlchemistTask():

    def __init__(self, model: GitAlchemistTaskModel, config: GitAlchemistConfig):
        self.model = model
        self.config = config
        self.next_step_ind = 0
        self.last_command = None

    def execute_next_step(self, skip_commands: List[str] = []):
        if self.next_step_ind == 0:
            logger.debug("")
            logger.debug(f"{'='*25} STARTING EXECUTION OF {self.model.title.upper()} {'='*25}")
            logger.debug("")
        try:
            list_entry = self.model.commands[self.next_step_ind]
        except IndexError:
            return
        self.next_step_ind += 1
        cmd_name, base_command = list(list_entry.items())[0]

        if cmd_name in skip_commands:
            logger.debug(f"Skipping step {self.next_step_ind}/{len(self.model.commands)}"
                         + f" of {self.model.title} (is in skip_commands)")
            return

        # current step as info
        logger.info(f"Executing step {self.next_step_ind}/{len(self.model.commands)}"
                    + f" of {self.model.title} | {base_command.__class__.__name__}")

        # add parameters for this step as debug
        logger.debug("-"*70)
        cmd_params = base_command.dict().copy()  # we don't need cmd_type in the log
        del cmd_params["cmd_type"]
        for k, v in cmd_params.items():
            _v = v
            if isinstance(v, list):
                _v = ", ".join([str(el) for el in v])
            logger.debug(f'  {k:<15}: {_v}')
        logger.debug("-"*70)
        base_command.__class__.execute(base_command, self.config)
        self.last_command = base_command

    def execute_next_n_steps(self, n: int):
        for _ in range(n):
            self.execute_next_step()

    def execute_remaining_steps(self, skip_commands: List[str] = []):
        while self.next_step_ind < len(self.model.commands):
            self.execute_next_step(skip_commands)

    @staticmethod
    def parse(config: GitAlchemistConfig):
        path_to_configfile = Path.joinpath(config.config_dir, config.task, "gitalchemist.yaml")
        return GitAlchemistTask(GitAlchemistTaskModel(
            **yaml.safe_load(path_to_configfile.read_text())),
            config
        )
