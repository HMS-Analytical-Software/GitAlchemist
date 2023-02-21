# %% 
from pathlib import Path
import shutil
import subprocess
import os
import yaml
import pdb
import time
from autogit.task import AutoGitTask
from autogit.task_model import AutoGitTaskModel
from autogit.config_model import AutoGitConfig
from autogit.config_env import git_path


working_dir = os.path.join("cwd", "cwd", f"{time.time()}")

# delete everything in the working dirs if possible (does not work sometimes, 
# just wait and delete later)
shutil.rmtree('cwd', ignore_errors=True)

my_task = "init_bare_repo"


config = AutoGitConfig(
    task=my_task,
    root_dir=os.getcwd(),
    config_dir=Path("test_configs"), 
    working_dir=working_dir,
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

task = AutoGitTask.parse(config)
task.execute()

