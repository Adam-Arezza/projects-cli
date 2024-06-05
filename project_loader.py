import subprocess
from abc import ABC, abstractmethod


class ProjectLoader(ABC):
    def __init__(self, project_path):
        self.project_path = project_path

    @abstractmethod
    def open_project(self, python_env=None):
        pass


class WindowsPojectLoader(ProjectLoader):
    def open_project(self, python_env=None):
        if python_env:
            cmd = [
                   "powershell.exe",
                   "-NoExit",
                   "-Command",
                  f"cd {self.project_path}; {python_env};" 
                   "wt",
                   "split-pane",
                   "-V",
                   "powershell.exe",
                   "-NoExit",
                   "-Command",
                   f"cd {self.project_path}; {python_env}; nvim ."
                   ]
            subprocess.run(cmd)
        else:
            cmd = [
                   "powershell.exe",
                   "-NoExit",
                   "-Command",
                   f"cd {self.project_path};"
                   "nvim ."
                   ]
            subprocess.run(cmd)

class UnixProjectLoader(ProjectLoader):
    #gnome-terminal -- bash -c "source /path/to/your/venv/bin/activate && python -c 'import sys; print(sys.executable)' && exec bash"
    #the command to open a new terminal and source the python environment if it exists
    def open_project(self, python_env):
         if python_env:
            cmd = ["gnome-terminal",
                   "--working-directory=",
                   f"{self.project_path}",
                   "-e", f"{python_env}",
                   "--tab",
                   "--working-directory=",
                   f"{self.project_path}",
                   "-e", f"{python_env}",
                   ]
            subprocess.run(cmd)
         else:
            cmd = ["wt",
                   "-d",
                   f"{self.project_path}",
                   "powershell.exe",
                   "-NoExit",
                   ";",
                   "split-pane",
                   "-V",
                   "-d",
                   f"{self.project_path}",
                   "powershell.exe",
                   "-NoExit",
                   ]
    
