import hashlib
from pathlib import Path

from autogit.config_model import AutoGitConfig
from autogit.git_config_settings import AUTHORS, EMAILS, DEFAULTBRANCH

class ConfigBuilder:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def create(self, task_name, config_dir: Path, rel_working_dir: Path) -> AutoGitConfig:
        self.config_dir = config_dir
        self.working_dir = self.root_dir / rel_working_dir
        config = AutoGitConfig(
            task=task_name,
            root_dir=self.root_dir,
            config_dir=self.config_dir,
            working_dir=self.working_dir,
            authors=AUTHORS,
            emails=EMAILS, 
            defaultBranch=DEFAULTBRANCH
        )
        return config


def hashfile(file):
    hash = hashlib.sha256()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()
