r'''
# GitAlchemist

This CLI tool creates bare repositories from config files on
local disc with a pre-defined history of commits. The primary purpose of this tool
is setting up interactive tasks for git workshops or git tutorials.

Please consult the readme file for more information on how to create
gitalchemist.yaml config files.

## Usage

Create tasks from default location (./configs):

- All: `main.py --run-all`
- Single: `main.py --task task_name`

Create tasks from custom folder (./my/dir):

- All: `main.py --config-dir ./my/dir --run-all`
- Single: `main.py --config-dir ./my/dir --task task_name`

Results will be stored in ./cwd/__timestamp__ where __timestamp__
increase with each run. Consider removing the ./cwd directory
in case you experience any trouble.
'''

__author__ = "HSM Analytical Software"
__copyright__ = "HSM Analytical Software"
__license__ = "GPLv3"
__version__ = "1.0.0"
__email__ = "info@analytical-software.de"

import argparse
import logging
import os
import shutil
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import List

from gitalchemist.config_model import GitAlchemistConfig
from gitalchemist.task import GitAlchemistTask
from gitalchemist.git_config_settings import AUTHORS, EMAILS, DEFAULTBRANCH


def setup_logging(level):
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("gitalchemist.log"),
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
    """
    GitAlchemist main function

    Args:
        config_dir (Path): Where the config files are stored (gitalchemist.yaml etc)
        tasks (List): List of task to execute
    """
    defaultBranchSet = os.popen("git config --get init.defaultBranch").read().strip()
    if defaultBranchSet != "" or defaultBranchSet != "main" or defaultBranchSet != DEFAULTBRANCH:
        warnings.warn(f"""Git seems to not be configured to use 'main' as the default init branch name: 
                      Querying 'git config --get init.defaultBranch' returned {defaultBranchSet}. 
                      This can lead to breakage of the program which currently assumes that branches 
                      are be called 'main'. Support for other default branch names will be added in 
                      the future.""")

    logger = logging.getLogger(__name__)

    # git is required; abort if not found
    if shutil.which("git") is None:
        raise RuntimeError("No git executable found, aborting.")

    # cleanup the working directory
    shutil.rmtree('cwd', ignore_errors=True)

    # create a new working directory within the cwd directory
    now = datetime.now()
    working_dir = os.path.join("cwd", f"{now.strftime('%Y%m%d_%H%M%S') + '_' + now.strftime('%f')[:3]}")

    # then iterate over all tasks and run GitAlchemistTask
    for task in tasks:
        logger.info("")
        logger.info(f"============== RUNNING GITALCHEMIST TASK {task} ==============")
        logger.info("")
        config = GitAlchemistConfig(
            task=task,
            root_dir=os.getcwd(),
            config_dir=config_dir,
            working_dir=working_dir,
            authors=AUTHORS,
            emails=EMAILS, 
            defaultBranch=DEFAULTBRANCH
        )
        task = GitAlchemistTask.parse(config)
        task.execute_remaining_steps()

    logger.info("")
    logger.info("============== GITALCHEMIST TASKS FINISHED SUCCESSFULLY ==============")


if __name__ == "__main__":

    args = setup_argparse().parse_args()

    # initialize logging (-v option)
    if args.verbose:
        setup_logging(logging.DEBUG)
    else:
        setup_logging(logging.INFO)

    # get the tasks to be executed
    tasks = [args.task] if not args.run_all else []
    if args.run_all:
        tasks = [str(x.name) for x in args.config_dir.iterdir() if x.is_dir()]

    # run gitalchemist
    main(
        config_dir=args.config_dir,
        tasks=tasks
    )
