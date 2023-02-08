from pathlib import Path
import shutil
import subprocess
import streamlit as st
import os
import time
from streamlit_ace import st_ace
from autogit.task import AutoGitTask
from autogit.config_model import AutoGitConfig

st.set_page_config(layout="wide")
st.title('Autogit')


working_dir=f'cwd\\cwd_{time.time()}'
gitbash = "C:\\Program Files\\Git\\git-bash.exe"


# delete everything in the working dirs if possible (does not work sometimes, 
# just wait and delete later)
shutil.rmtree('cwd', ignore_errors=True)

# streamlit stuff starts here
c1, c2 = st.columns((1,4))

def run_task(task: str):
    config = AutoGitConfig(
        root_dir=os.getcwd(),
        working_dir=working_dir,
        task=task,
        authors={
            'red': 'Richard Red <richard@pw-compa.ny>',
            'blue': 'Betty Blue <betty@pw-compa.ny>',
            'green': 'Garry Green <garry@pw-compa.ny>',
        }
    )
    # execute the task
    task = AutoGitTask.parse(config)
    task.execute()

with c1:
    st.button("run")

    tasks = []
    for path in Path(os.getcwd()).joinpath('configs').iterdir():
        if path.is_dir():
            tasks.append(path.name)

    task_name = st.selectbox('Tasks', ['Select Task'] + tasks)

    if st.button("run all"):
        for file in Path(os.getcwd()).joinpath('configs').glob("*"):
            if file.joinpath("autogit.yaml").exists():
                run_task(file.name)


    with c2: 
        terminal = st.checkbox('Open Git-Bash Terminal', value=True)

    if task_name != 'Select Task':

        with c2: 
            configfile = Path(os.getcwd()).joinpath('configs').joinpath(task_name).joinpath("autogit.yaml")
            value = st_ace(value=configfile.read_text(), language="yaml")
            configfile.write_text(value)
        
        config = AutoGitConfig(
            root_dir=os.getcwd(),
            working_dir=working_dir,
            task=task_name,
            authors={
                'red': 'Richard Red <richard@pw-compa.ny>',
                'blue': 'Betty Blue <betty@pw-compa.ny>',
                'green': 'Garry Green <garry@pw-compa.ny>',
            }
        )
        # execute the task
        task = AutoGitTask.parse(config)
        task.execute()

with c2: 
    if terminal and task_name != 'Select Task':
        try:
            print("open git bash")
            subprocess.call([gitbash , f"--cd={os.getcwd()}\\{working_dir}\\{config.current_repo}"])
        except:
            print("git-bash.exe not found")

    
