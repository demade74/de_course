import shutil
from os import mkdir, makedirs, chdir, walk, scandir
from os.path import exists, basename, join

PROJECT_ROOT = 'my_project'
# create templates dir in main dir
templates_path = join(PROJECT_ROOT, 'templates')
if not exists(templates_path):
    mkdir(templates_path)

# copy files
for root, dirs, files in walk(PROJECT_ROOT):
    if basename(root) == 'templates':
        if root == templates_path:
            continue
        else:
            for entry in scandir(root):
                if entry.is_dir():
                    destination_path = join(templates_path, entry.name)
                    if not exists(destination_path):
                        mkdir(destination_path)
                    for template_file in scandir(entry.path):
                        shutil.copy2(template_file.path, destination_path)

                    
                
