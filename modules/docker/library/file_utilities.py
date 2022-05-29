import logging
from pathlib import Path
import os

class FileUtilities:

    # TODO Move to library
    @staticmethod
    def list_dirs(from_dir=".", containing_files=[], logger=logging.getLogger('list_dirs')) -> list:
        entries = None
        logger.debug(f'Check {from_dir} with files {containing_files}')
        try:
            entries = os.scandir(from_dir)
        except Exception as e:
            logger.error(e)
            return []
        dirs = []
        for entry in entries:
            if entry.is_dir():
                directory = entry.name
                all_files_present = True
                for file_to_search in containing_files:
                    checked_file_path = os.path.join(os.path.join(from_dir,directory), file_to_search)
                    file_exist = os.path.exists(checked_file_path)
                    logger.debug(f'Does {checked_file_path} exist ? {file_exist}')
                    all_files_present &= file_exist

                if all_files_present:
                    dirs.append(directory)
        return dirs
