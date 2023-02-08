import yaml
from pathlib import Path
from autogit.config_model import AutoGitConfig
from autogit.task_model import AutoGitTaskModel


class AutoGitTask():

    def __init__(self, model: AutoGitTaskModel, config: AutoGitConfig):
        self.model = model
        self.config = config

    def execute(self, skip_commands=[]):
        print("run task", self.model.title)
        cnt = 1
        for list_entry in self.model.commands:
            for cmd_name, base_command in list_entry.items():
                if cmd_name in skip_commands:
                    base_command.log("skip (is in skip_commands)")
                    continue
                cmd_params = base_command.dict().copy()
                # we don't need this in the log below
                del cmd_params["cmd_type"]
                print("-"*30)
                print(
                    f"{self.model.title} step {cnt}/{len(self.model.commands)} | {base_command.__class__.__name__} | {str(cmd_params)}")
                print("-"*30)
                base_command.__class__.execute(base_command, self.config)
                cnt += 1

    @staticmethod
    def parse(config: AutoGitConfig):
        path = Path(f"./configs/{config.task}/autogit.yaml")
        return AutoGitTask(AutoGitTaskModel(
            **yaml.safe_load(path.read_text())),
            config
        )
