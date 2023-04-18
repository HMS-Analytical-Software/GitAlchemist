import pytest
from .utils import ConfigBuilder
import shutil
import time
from pathlib import Path

@pytest.fixture
def config_builder(tmp_path):
    return ConfigBuilder(root_dir=tmp_path)

assert shutil.which("git") is not None, "No git executable found, aborting."
my_config_dir = Path("test_configs").resolve()
my_rel_working_dir = Path("cwd", f"{time.time()}")
