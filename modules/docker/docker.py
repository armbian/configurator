import logging
import os
from pathlib import Path
import shutil
import sys

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from renderers.qt.widgets import SelectionMenu, provide_user_choice

logging.basicConfig(level=logging.DEBUG)

config = {
    'templates_dir': '/usr/share/armbian/configurator/modules/docker/softwares',
    'install_dir': '/opt/armbian/docker',
    'install': [],
    'remove': []
}

def list_dirs(from_dir=".", containing_files=[]) -> list:
    entries = None
    try:
        entries = os.scandir(from_dir)
    except:
        return []
    dirs = []
    for entry in entries:
        if entry.is_dir():
            directory = entry.name
            all_files_present = True
            for file_to_search in containing_files:
                checked_file_path = os.path.join(os.path.join(from_dir,directory), file_to_search)
                file_exist = os.path.exists(checked_file_path)
                print(f'Does {checked_file_path} exist ? {file_exist}')
                all_files_present &= file_exist
            
            if all_files_present:
                dirs.append(directory)
    return dirs

class Module:
    def __init__(self, configuration):
        self.configuration = configuration

    def docker_install(self, configuration=None):
        configuration = self.configuration if configuration == None else configuration
        if len(configuration["install"]) == 0:
            print('No docker to install')
            return
        install_path = Path(configuration["install_dir"])
        templates_path = Path(configuration["templates_dir"])
        try:
            install_path.mkdir( mode=0o755, parents=True, exist_ok=True )
        except Exception as e:
            print(f'mkdir -p {install_path} failed: ')
            print(e)
            sys.exit(1)

        print(configuration)
        for selected_dir in configuration["install"]:
            shutil.copytree((templates_path / selected_dir), (install_path / selected_dir))

    def docker_remove(self, configuration=None):
        configuration = self.configuration if configuration == None else configuration
        install_path = Path(configuration["install_dir"])
        if len(configuration["remove"]) is 0:
            print('No docker to remove')
            return

        for dir_to_remove in configuration["remove"]:
            remove_path = install_path / dir_to_remove
            try:
                shutil.rmtree(remove_path)
            except Exception as e:
                print(f'Could not delete {remove_path}')
                continue

    def run(self):
        self.docker_remove()
        self.docker_install()
        
def module_payload(configuration):
    docker_install(configuration["install"])

if __name__ == '__main__':
    # TODO : Parse from configuration file
    available_dockers = list_dirs(config["templates_dir"], ['docker-compose.yml'])
    installed_dockers = list_dirs(config["install_dir"], ['docker-compose.yml'])
    images_list = '\n\t' + '\n\t'.join(available_dockers)
    parser = ArgumentParser(description='Armbian docker installation module', formatter_class=RawDescriptionHelpFormatter, epilog='IMAGES :' + images_list)
    parser.add_argument('--install', nargs='+', metavar='IMAGE', choices=available_dockers, help='Add docker installations')
    parser.add_argument('--templates-dir', nargs='?', default=config['templates_dir'], help='Directory path to list templates from')
    parser.add_argument('--install-dir', nargs='?', default=config['install_dir'], help='Directory path where docker images are installed')
    args = parser.parse_args()
    
    install_dir = args.install_dir
    templates_dir = args.templates_dir
    
    if args.install == None or len(args.install) == 0:
        try:
            installed_set = set(installed_dockers)
            selected, unselected = provide_user_choice(available_dockers, installed_set)
            available_set = set(available_dockers)
            
            print(f'selected: {selected} - unselected: {unselected}')
            to_install = (selected - installed_set)
            to_remove = (installed_set & unselected)
            print(f'Install : {to_install}, Remove: {to_remove}')
            config["install"] = to_install
            config["remove"] = to_remove
            Module(config).run()

        except Exception as e:
            parser.print_help()
            print(f'A problem araised {e}')

