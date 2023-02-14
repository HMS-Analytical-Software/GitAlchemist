# Autogit

Autogit is a small framework for creating bare repositories from config files with a pre-defined history of commits. The primary purpose of this tool is setting up local git environments for teaching purposes, i.e. git workshops. At the core of this tool are so-called `autogit.yaml` files which define a series of actions for virtual (fake) users like creating files or executing git commands.

## Example

The below example will create a git repository with two commits.

- The first command creates a bare (local) git repository called example_repo. It will
  also create a working directory that clones from this new bare repo.
- The second command takes a pre-defined file that is stored in
  configs/taskXYZ/files/readme.md (source) and puts it to the working
  directory under the name readme.md (target). It then adds the file via `git add`
  followed by `git commit` with the specified commit message.
- The third command does the same for another file
- The last command pushes the working directory to the bare repo

```yaml
title: Example Task
commands:
  -
    init_bare_repo:
      name: example_repo
  -
    create_add_commit:
      source: files/readme.md
      target: readme.md
      message: added readme
      author: red
  -
    create_add_commit:
      source: files/main.py
      target: main.py
      message: added a main.py file
      author: red 
  -
    git:
      command: "git push origin master"  
```

## Getting Started

Assuming windows as dev environment you can execute the tool as follows after you
cloned the repo (tested only with Python 3.10):

```bash
py -m venv venv
. venv/scripts/activate
pip install streamlit streamlit-ace pydantic pyyaml
streamlit run ./main.py
```

Git for windows must be installed or the tool will not work.
