from pathlib import Path

import yaml

from autogit.config_model import AutoGitConfig
from autogit.task_model import AutoGitTaskModel


class AutoGitTask():

    def __init__(self, model: AutoGitTaskModel, config: AutoGitConfig):
        self.model = model
        self.config = config
        self.next_step_ind = 0

    def execute_next_step(self, skip_commands=[]):
        if self.next_step_ind == 0:
            print(f"\n{'='*25} STARTING EXECUTION OF {self.model.title.upper()} {'='*25}")
        try:
            list_entry = self.model.commands[self.next_step_ind]
        except IndexError:
            return
        self.next_step_ind += 1
        assert len(list_entry) == 1
        cmd_name, base_command = list(list_entry.items())[0]

        if cmd_name in skip_commands:
            print(f"Skipping step {self.next_step_ind}/{len(self.model.commands)} of {self.model.title} (is in skip_commands)")
            return
        
        cmd_params = base_command.dict().copy()
        # we don't need this in the log below
        del cmd_params["cmd_type"]
        print(f"\nExecuting step {self.next_step_ind}/{len(self.model.commands)} of {self.model.title} | {base_command.__class__.__name__} | {str(cmd_params)}")
        print("-"*70)
        base_command.__class__.execute(base_command, self.config)
        self.last_command = base_command
    
    def execute_next_n_steps(self, n):
        for _ in range(n):
            self.execute_next_step()

    def execute_remaining_steps(self, skip_commands=[]):
        while self.next_step_ind < len(self.model.commands):
            self.execute_next_step(skip_commands)

    @staticmethod
    def parse(config: AutoGitConfig):
        path_to_configfile = Path.joinpath(config.config_dir, config.task, "autogit.yaml")
        return AutoGitTask(AutoGitTaskModel(
            **yaml.safe_load(path_to_configfile.read_text())),
            config
        )
