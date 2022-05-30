from abc import ABC, abstractmethod
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import logging
from pathlib import Path
import os
import shutil
import subprocess
import sys

from .file_utilities import FileUtilities

class SystemServicesHandler(ABC):
    @abstractmethod
    def start(self, service_name:str):
        raise NotImplementedError

    @abstractmethod
    def stop(self, service_name:str):
        raise NotImplementedError

    @abstractmethod
    def status(self, service_name:str):
        raise NotImplementedError

    @abstractmethod
    def add_on_boot(self, service_name:str):
        raise NotImplementedError

    @abstractmethod
    def remove_from_boot(self, service_name:str):
        raise NotImplementedError

class SystemDServicesHandler(SystemServicesHandler):

    def systemd(self, action_name:str, service_name:str):
        print(subprocess.run(["systemctl", action_name, service_name]))

    def start(self, service_name:str):
        self.systemd("start", service_name)

    def stop(self, service_name:str):
        self.systemd("stop", service_name)

    def status(self, service_name:str):
        self.systemd("status", service_name)

    def add_on_boot(self, service_name:str):
        self.systemd("enable", service_name)

    def remove_from_boot(self, service_name:str):
        self.systemd("disable", service_name)

class DockerComposeModule:
    MAIN_PATH=Path('/opt/armbian/docker')
    DOCKER_SERVICE_NAME="docker"

    # configuration :
    #  install_dir: Path where docker services should be installed
    #  templates_dir: Path where docker services are available from

    def __init__(self, configuration):
        self.configuration = configuration
        configuration["install_dir"] = Path(configuration["install_dir"])
        configuration["templates_dir"] = Path(configuration["templates_dir"])
        self.logger = logging.getLogger('docker-compose module')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.services_handler = SystemDServicesHandler()

    def installed_path(self, service_name:str):
        return (self.configuration["install_dir"] / service_name)

    # FIXME This is a very weak way to check for installations
    def is_installed(self, service_name:str):
        return self.installed_path(service_name).exists()


    @staticmethod
    def list_installed(configuration) -> list:
        return FileUtilities.list_dirs(
            from_dir = configuration["install_dir"],
            containing_files = ["docker-compose.yml"])

    @staticmethod
    def list_available(configuration) -> list:
        return FileUtilities.list_dirs(
            from_dir = configuration["templates_dir"],
            containing_files = ["docker-compose.yml"])

    def compose_yaml_path(self, service_name: str):
        return self.configuration['install_dir'] / service_name / 'docker-compose.yml'

    def docker_compose_get_content(self, services_names:list) -> list:
        ret = []
        if not services_names:
            self.logger.debug('No service provided...')
            return ret

        install_path = self.configuration['install_dir']

        for service_name in services_names:
            content = ''
            with open(self.compose_yaml_path(service_name), 'r') as compose_file:
                content = compose_file.read()
            ret.append(content)

        return ret

    # TODO Check if the service name is actually available ?
    def docker_install(self, services_names:list):
        if not services_names:
            self.logger.debug('No docker to install')
            return

        install_path = self.configuration["install_dir"]
        templates_path = self.configuration["templates_dir"]

        try:
            install_path.mkdir( mode=0o755, parents=True, exist_ok=True )
        except Exception as e:
            self.logger.error(f'mkdir -p {install_path} failed: ')
            self.logger.error(e)
            sys.exit(1)

        for service_name in services_names:
            shutil.copytree((templates_path / service_name), (install_path / service_name))

    def docker_remove(self, services_names:list):
        if not services_names:
            self.logger.debug('No docker to remove')
            return

        for docker_compose_service in services_names:
            remove_path = self.installed_path(docker_compose_service)
            if remove_path.exists():
                try:
                    shutil.rmtree(remove_path)
                except Exception as e:
                    self.logger.error(f'Could not delete {remove_path}')
                    continue
            else:
                self.logger.error(f'{remove_path} does not exist. Skipping {docker_compose_service}')
                continue

    def service_path(self, service_name: str, specific_file_path: str) -> Path:
        returned_path = Path(self.MAIN_PATH / service_name)
        if specific_file_path:
            returned_path = Path(returned_path / specific_file_path)
        return returned_path

    def output_script_result(self, tool_name: str, args: []) -> tuple:
        self.logger.debug(args)
        process_result = subprocess.run([f'tools/{tool_name}'] + args, capture_output=True, text=True)
        return (process_result.stdout, process_result.stderr)

    def docker_service_start(self):
        self.services_handler.start(self.configuration['service_name'])

    def docker_service_stop(self):
        self.services_handler.stop(self.configuration['service_name'])

    def docker_service_status(self):
        self.services_handler.status(self.configuration['service_name'])

    def docker_service_add_on_boot(self):
        self.services_handler.add_on_boot(self.configuration['service_name'])

    def docker_service_remove_from_boot(self):
        self.services_handler.remove_from_boot(self.configuration['service_name'])

    # TODO Factorize
    def compose_status(self, services_names: list):
        ret = []
        if not services_names:
            self.logger.debug('No services provided for status')
            return ret

        for service_name in services_names:
            self.logger.info(f'Showing {service_name} status')
            outputs = self.output_script_result(
                tool_name = "compose_status.sh",
                args = [self.service_path(service_name, "docker-compose.yml")])
            ret.append(outputs)

        return ret

    def compose_start(self, services_names: list):
        ret = []
        if not services_names:
            self.logger.debug('No services provided for start')
            return ret

        for service_name in services_names:
            self.logger.info(f'Starting {service_name}')
            outputs = self.output_script_result(
                tool_name = "compose_start.sh",
                args = [self.service_path(service_name, "docker-compose.yml")])
            ret.append(outputs)

        return ret

    def compose_stop(self, services_names: list):
        ret = []
        if not services_names:
            self.logger.debug('No services provided for stop')
            return ret

        for service_name in services_names:
            self.logger.info(f'Stopping {service_name}')
            outputs = self.output_script_result(
                tool_name = "compose_stop.sh",
                args = [self.service_path(service_name, "docker-compose.yml")])
            ret.append(outputs)

        return ret
