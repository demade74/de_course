import yaml
import pprint
import shutil
from os import mkdir, makedirs, chdir
from os.path import exists

project_root = ''

with open('project_structure.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

def create_structure_processing(structure):
    global project_root
    for key, value in structure.items():
        # check for existing project
        if not project_root:
            project_root = key
            if exists(project_root):
                user_input = input(f"Project with name {project_root} already exists\nDo you want re-create project?\ntype 'y' if you want, 'n' otherwise ")
                if user_input == 'y':
                    shutil.rmtree(project_root)
                else:
                    exit(0)

        # main processing
        if not exists(key):
            mkdir(key)
            chdir(key)
        if isinstance(value, dict):
            create_structure_processing(value)
        else:
            for item in value:
                if isinstance(item, dict):
                    create_structure_processing(item)
                else:
                    open(item, 'a').close()
            chdir('..')

create_structure_processing(data)
