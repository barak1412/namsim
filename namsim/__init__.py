from namsim.data import get_data_path
from namsim.constants import DEFAULT_CONF_DIRECTORY
from namsim.base import Namsim
import os
import fnmatch


# replacing stub paths in the configurations
_STUB_PATH_NAME = 'STUB_PATH'


def configuration_paths_rename():
    # set conf path and replace slash to backslash to support UNIX systems
    conf_dir_path = get_data_path(DEFAULT_CONF_DIRECTORY)
    conf_dir_path = conf_dir_path.replace(os.sep, '/')

    # change paths in all conf .xml files
    file_pattern = "*.xml"
    for path, dirs, files in os.walk(conf_dir_path):
        for filename in fnmatch.filter(files, file_pattern):
            full_file_path = os.path.join(path, filename)

            # replace stub with the actual paths
            # Read in the file
            with open(full_file_path, 'r') as file:
                file_data = file.read()

            # Replace the target string and fix slash direction based
            file_data = file_data.replace(_STUB_PATH_NAME, conf_dir_path)

            # Write the file out again
            with open(full_file_path, 'w') as file:
                file.write(file_data)


configuration_paths_rename()