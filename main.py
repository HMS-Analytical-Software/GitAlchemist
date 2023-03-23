# %% 
import os
import shutil
import time
from pathlib import Path

from autogit.config_model import AutoGitConfig
from autogit.task import AutoGitTask

assert shutil.which("git") is not None, "No git executable found, aborting."

# delete everything in the working dirs if possible (does not work sometimes, 
# just wait and delete later)
shutil.rmtree('cwd', ignore_errors=True)

working_dir = os.path.join("cwd", f"{time.time()}")
config_dir = Path("configs") 
my_task = "task_fail"

config = AutoGitConfig(
    task=my_task,
    root_dir=os.getcwd(),
    config_dir=config_dir, 
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
task.execute_remaining_steps()

print("============== AUTOGIT TASKS FINISHED SUCCESSFULLY ==============")
