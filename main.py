import argparse
import logging
import os
import shutil
import sys
import time
from pathlib import Path
from typing import List

from autogit.config_model import AutoGitConfig
from autogit.task import AutoGitTask

AUTHORS = {
    'red': 'Richard Red <richard@pw-compa.ny>',
    'blue': 'Betty Blue <betty@pw-compa.ny>',
    'green': 'Garry Green <garry@pw-compa.ny>',
}

EMAILS = {
    'red': 'richard@pw-compa.ny',
    'blue': 'betty@pw-compa.ny',
    'green': 'garry@pw-compa.ny',
}


def setup_logging(level):
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("autogit.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-dir",
                        type=Path,
                        default=Path("configs"),
                        help="directory containing the task configuration files (default: configs)")
    parser.add_argument("-v", "--verbose",
                        default=False,
                        action='store_true',
                        help="debug output is shown when this flag is used")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--task",
                       type=str,
                       default="task1",
                       help="task to run (default: task1)")
    group.add_argument("--run-all",
                       action="store_true",
                       help="run all tasks in the configuration directory")

    return parser


def main(config_dir: Path, tasks: List):
    """Autogit main function

    Args:
        config_dir (Path): Where the config files are stored (autogit.yaml etc)
        tasks (List): List of task to execute
    """

    logger = logging.getLogger(__name__)

    # git is required; abort if not found
    if shutil.which("git") is None:
        raise RuntimeError("No git executable found, aborting.")

    # cleanup the working directory
    shutil.rmtree('cwd', ignore_errors=True)

    # create a new working directory within the cwd directory
    working_dir = os.path.join("cwd", f"{time.time()}")

    # then iterate over all tasks and run AutoGitTask
    for task in tasks:
        logger.info("")
        logger.info(f"============== RUNNING AUTOGIT TASK {task} ==============")
        logger.info("")
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

    logger.info("")
    logger.info("============== AUTOGIT TASKS FINISHED SUCCESSFULLY ==============")


if __name__ == "__main__":

    args = setup_argparse().parse_args()

    # initialize logging using verbose settings (-v option)
    if args.verbose:
        setup_logging(logging.DEBUG)
    else:
        setup_logging(logging.INFO)

    # get the tasks to be executed
    tasks = [args.task] if not args.run_all else []
    if args.run_all:
        tasks = [str(x.name) for x in args.config_dir.iterdir() if x.is_dir()]

    # run autogit
    main(
        config_dir=args.config_dir,
        tasks=tasks
    )
