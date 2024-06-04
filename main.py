import os
import pyfiglet
import inquirer
import shutil
import json
import subprocess
from colorama import Fore, Back, Style
from pathlib import Path


cli_header = pyfiglet.figlet_format("Projects-CLI")
main_menu = [inquirer.List("action", 
                           message="select an option to continue, if this is the first time using the tool select 'setup'", 
                           choices=["setup",
                                    "list projects", 
                                    "add project", 
                                    "remove project", 
                                    "open project",
                                    "quit"])]
PROJECTS = str(Path.home()) + "\\project_cli"
quit_flag = False
o_s = os.name
print(o_s)


def setup():
    global PROJECTS
    if not os.path.isdir(PROJECTS):
        os.umask(0)
        os.mkdir(PROJECTS, mode=0o777)
    else:
        yes_no = [inquirer.List("action", choices=["Yes", "No"])]
        print("found a projects list directory has already been created...")
        print("do you want to overwrite it? This will remove any project lists that were there.")
        y_n = inquirer.prompt(yes_no)
        if y_n:
            if y_n["action"] == "Yes":
                os.umask(0)
                shutil.rmtree(PROJECTS)
                os.mkdir(PROJECTS, mode=0o777)
            else:
                print("Kept project list, select a different option.")
                return


def list_projects():
    with open(PROJECTS+"\\projects.json", "r") as projects_file:
        projects = json.load(projects_file)
        projects_file.close()
    print("project list: ")
    for p in projects:
        print(p)


def add_project():
    project_name = input("Enter a name for the project: \n")
    project_dir = input("Enter the path to the project directory: \n")
    projects = []
    if not "projects.json" in os.listdir(PROJECTS):
        print("creating projects.json file...")
        with open(PROJECTS+"\\projects.json", "w") as project_file:
            new_project = {"name":project_name, "path":project_dir}
            projects.append(new_project)
            new_project_list = json.dumps(projects)
            project_file.write(new_project_list)
            project_file.close()
    else:
        print("reading projects list...")
        with open(PROJECTS+"\\projects.json", "r") as project_file:
            projects = json.load(project_file)
            print(projects)
            project_file.close()

        with open(PROJECTS+"\\projects.json", "w") as project_file:
            new_project = {"name":project_name, "path":project_dir}
            projects.append(new_project)
            new_project_list = json.dumps(projects)
            project_file.write(new_project_list)
            project_file.close()
    print(f"added project: {project_name} to the projects list.")


def remove_project():
    with open(PROJECTS+"\\projects.json", "r") as projects_file:
        projects = json.load(projects_file)
        projects_file.close()

    remove_list = [inquirer.List("action", choices=[i['name'] for i in projects])]
    remove_prompt = inquirer.prompt(remove_list)
    print(projects)
    if remove_prompt:
        for i in range(len(projects)):
            name = projects[i]['name']
            if remove_prompt["action"] == projects[i]['name']:
                projects.pop(i)
                print(f"removed project: {name}")
                break
    with open(PROJECTS+"\\projects.json", "w") as project_file:
            new_project_list = json.dumps(projects)
            project_file.write(new_project_list)
            project_file.close()


def open_project():
    with open(PROJECTS+"\\projects.json", "r") as projects_file:
        projects = json.load(projects_file)
        projects_file.close()
    project_list = [inquirer.List("action", choices=[i['name'] for i in projects])]
    open_prompt = inquirer.prompt(project_list)
    if open_prompt:
        project_path = None
        env_script = None
        project_name = open_prompt["action"]
        for i in range(len(projects)):
            if projects[i]['name'] == project_name:
                project_path = projects[i]['path']
        if "env" in os.listdir(project_path):
            env_script = ".\env\\Scripts\\activate"
        print(f"opening project:{project_name}")
        if env_script:
            cmd = ["wt",
                   "-d",
                   f"{project_path}",
                   "powershell.exe",
                   "-NoExit",
                   "-Command", f".\\{env_script}",
                   ";",
                   "split-pane",
                   "-V",
                   "-d",
                   f"{project_path}",
                   "powershell.exe",
                   "-NoExit",
                   "-Command", f".\\{env_script}",
                   ]
            subprocess.run(cmd)
        else:
            cmd = ["wt",
                   "-d",
                   f"{project_path}",
                   "powershell.exe",
                   "-NoExit",
                   ";",
                   "split-pane",
                   "-V",
                   "-d",
                   f"{project_path}",
                   "powershell.exe",
                   "-NoExit",
                   ]
            subprocess.run(cmd)
        exit(0)


def set_quit():
    global quit_flag
    quit_flag = True


options = {"setup": setup,
           "list projects": list_projects,
           "add project": add_project,
           "remove project": remove_project,
           "open project": open_project,
           "quit": set_quit
           }


def main():
    print(Fore.GREEN, cli_header)
    print("Please select an option, use arrow keys to move up/down and ENTER on selection:")
    while not quit_flag:
        answers = inquirer.prompt(main_menu, raise_keyboard_interrupt=True)
        if answers:
            options[answers["action"]]()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("exiting")
        exit(0)
