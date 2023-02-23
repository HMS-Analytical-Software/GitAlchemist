from autogit.config_model import AutoGitConfig

class ConfigBuilder:
    def __init__(self, root_dir):#, config_dir, working_dir):
        self.root_dir = root_dir

    def create(self, task_name, config_dir, rel_working_dir):
        self.config_dir = config_dir
        self.working_dir = self.root_dir / rel_working_dir
        config = AutoGitConfig(
            task=task_name,
            root_dir=self.root_dir,
            config_dir=self.config_dir,
            working_dir=self.working_dir, 
            authors={
                'red': 'Richard Red <richard@pw-compa.ny>',
                'blue': 'Betty Blue <betty@pw-compa.ny>',
                'green': 'Garry Green <garry@pw-compa.ny>',
            },
            emails={
                'red': 'richard@pw-compa.ny',
                'blue': 'betty@pw-compa.ny',
                'green': 'garry@pw-compa.ny',
            }
        )
        return config

