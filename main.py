# %% 
import os
import shutil
import time
import argparse
from pathlib import Path
from typing import List

from autogit.config_model import AutoGitConfig
from autogit.task import AutoGitTask


AUTHORS={
    'red': 'Richard Red <richard@pw-compa.ny>',
    'blue': 'Betty Blue <betty@pw-compa.ny>',
    'green': 'Garry Green <garry@pw-compa.ny>',
}

EMAILS={
    'red': 'richard@pw-compa.ny',
    'blue': 'betty@pw-compa.ny',
    'green': 'garry@pw-compa.ny',
}

def setup_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-dir", 
                        type=Path, 
                        default=Path("configs"), 
                        help="The directory containing the task configuration files. (default: configs)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--task", 
                       type=str, 
                       default="task1", 
                       help="The task to run. (default: task1)")
    group.add_argument("--run-all", 
                       action="store_true", 
                       help="Run all tasks in the configuration directory.")
    args = parser.parse_args()
    tasks = [args.task] if not args.run_all else []

    return args.config_dir, tasks, args.run_all


def main(config_dir: Path, tasks: List, run_all: bool = False):
    assert shutil.which("git") is not None, "No git executable found, aborting."
    shutil.rmtree('cwd', ignore_errors=True)

    config_dir = config_dir
    working_dir = os.path.join("cwd", f"{time.time()}")
    if run_all:
        tasks = [str(x.name) for x in config_dir.iterdir() if x.is_dir()]

    for task in tasks:
        print("============== RUNNING AUTOGIT TASK", task, "==============")
        config = AutoGitConfig(
            task=task,
            root_dir=os.getcwd(),
            config_dir=config_dir, 
            working_dir=working_dir,
            authors=AUTHORS,
            emails=EMAILS
        )

        task = AutoGitTask.parse(config)
        task.execute_remaining_steps()


if __name__ == "__main__":
    config_dir, tasks, run_all = setup_argparse()
    main(config_dir=config_dir, tasks=tasks, run_all=run_all)
    print("============== AUTOGIT TASKS FINISHED SUCCESSFULLY ==============")
