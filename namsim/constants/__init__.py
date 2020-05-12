from pkg_resources import get_distribution
from namsim.data import get_data_path
import os

PACKAGE_NAME = 'namsim'
VERSION = get_distribution(PACKAGE_NAME).version
DEFAULT_CONF_DIRECTORY = 'default_namsim_conf'
DEFAULT_CONF_PATH = get_data_path(os.path.join(DEFAULT_CONF_DIRECTORY, 'conf', 'namsim_config.xml'))