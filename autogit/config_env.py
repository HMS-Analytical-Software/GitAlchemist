import os 

git_path = "C:\\Program Files\\Git\\git-bash.exe"

if not os.path.isfile(git_path):
    git_path = '/usr/bin/git'
