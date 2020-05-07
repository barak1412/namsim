import ctypes
from namsim.data import get_data_path
import platform
import os


def _get_handler(dll_name):
    # retrieve os ('windows' or 'linux')
    os_platform = str(platform.system()).lower()
    dll_dir = get_data_path(os.path.join('bin', os_platform))

    # load dll based on platform
    handler = None
    if os_platform == 'windows':
        dll_path = os.path.join(dll_dir, dll_name + '.dll')
    elif os_platform == 'linux':
        dll_path = os.path.join(dll_dir, dll_name + '.so')
    else:
        raise Exception('Unsupported platform: {}'.format(os_platform))

    handler = ctypes.cdll.LoadLibrary(dll_path)

    # set functions signature
    handler.NamsimInit.argtypes = [ctypes.c_int, ctypes.c_char_p]
    handler.NamsimInit.restype = ctypes.c_int

    handler.NamsimDone.argtypes = [ctypes.c_int]
    handler.NamsimDone.restype = ctypes.c_int

    handler.NamsimSimilarity.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]
    handler.NamsimSimilarity.restype = ctypes.c_int

    return handler


class NamsimWrapper(object):

    DLL_NAME = 'NAMSIMAPI'

    # static handler for the compiled library
    _handler = _get_handler(DLL_NAME)

    @staticmethod
    def _prepare_encoded_string(s):
        return s.encode('utf-16le') + b'\x00'

    @staticmethod
    def namsim_init(namsim_id, conf_path=None):
        if conf_path is None:
            conf_dir_name = 'default_namsim_conf'
            conf_path = get_data_path(os.path.join(conf_dir_name, 'conf', 'namsim_config.xml'))
        conf_path = NamsimWrapper._prepare_encoded_string(conf_path)

        return NamsimWrapper._handler.NamsimInit(namsim_id, conf_path)

    @staticmethod
    def namsim_done(namsim_id):
        return NamsimWrapper._handler.NamsimDone(namsim_id)

    @staticmethod
    def namsim_similarity(namsim_id, str1, str2):
        str1 = NamsimWrapper._prepare_encoded_string(str1)
        str2 = NamsimWrapper._prepare_encoded_string(str2)
        similarity = ctypes.c_double(0.0)

        error_code = NamsimWrapper._handler.NamsimSimilarity(namsim_id, str1, str2, ctypes.pointer(similarity))
        return error_code, similarity.value
