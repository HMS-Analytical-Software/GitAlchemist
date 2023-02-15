from pathlib import Path
import shutil
import subprocess
import os
import yaml
import time
from autogit.task import AutoGitTask
from autogit.task_model import AutoGitTaskModel
from autogit.config_model import AutoGitConfig
from autogit.config_env import git_path


working_dir = os.path.join("cwd", "cwd", f"{time.time()}")

# delete everything in the working dirs if possible (does not work sometimes, 
# just wait and delete later)
shutil.rmtree('cwd', ignore_errors=True)

my_task = "task0"


configfile = Path(os.getcwd()).joinpath('configs').joinpath(my_task).joinpath("autogit.yaml")

# import pdb; pdb.set_trace()

configfile.write_text(configfile.read_text())

config = AutoGitConfig(
    root_dir=os.getcwd(),
    working_dir=working_dir,
    task=my_task,
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

my_auto_git_task_model = AutoGitTaskModel(**yaml.safe_load(configfile.read_text()))
#import pdb; pdb.set_trace()

# execute the task
task = AutoGitTask.parse(config)
task.execute()
