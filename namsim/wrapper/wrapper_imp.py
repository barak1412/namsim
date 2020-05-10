import ctypes
from namsim.data import get_data_path
import platform
import os
from pkg_resources import get_distribution


def _get_handler(dll_prefix):
    # retrieve os ('windows' or 'linux')
    os_platform = str(platform.system()).lower()
    dll_dir = get_data_path(os.path.join('bin', os_platform))

    # load dll based on platform
    handler = None
    platform_letter = None
    platform_dll_type = None
    if os_platform == 'windows':
        platform_letter = 'W'
        platform_dll_type = 'dll'
    elif os_platform == 'linux':
        platform_letter = 'L'
        platform_dll_type = 'so'
    else:
        raise Exception('Unsupported platform: {}'.format(os_platform))

    version_major = get_distribution('namsim').version.split('.')[0]
    version_minor = get_distribution('namsim').version.split('.')[1]
    dll_name = '{}_{}64_{}_{}.{}'.format(dll_prefix, platform_letter, version_major, version_minor, platform_dll_type)
    dll_path = os.path.join(dll_dir, dll_name)
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

    DLL_NAME = 'NamsimCAPI'
    MAX_BUFFER_LENGTH = 256

    # static handler for the compiled library
    _handler = _get_handler(DLL_NAME)

    @staticmethod
    def _prepare_encoded_string(s):
        return s.encode('utf-16le') + b'\x00'

    @staticmethod
    def _decode_buffer(buff):
        address = ctypes.addressof(buff)
        chars = []
        i = 0
        while i < NamsimWrapper.MAX_BUFFER_LENGTH*2+1:
            c1 = ctypes.c_char.from_address(address).value
            c2 = ctypes.c_char.from_address(address+1).value
            if c1 == b'\x00' and c2 == b'\x00':
                break
            chars += [c1, c2]
            address += 2
            i += 1
        return b''.join(chars).decode('utf-16le')

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

    @staticmethod
    def get_error_message(error_code):
        NamsimWrapper._handler.GetErrorMessage.argtypes = [ctypes.c_int, ctypes.c_char_p]
        NamsimWrapper._handler.GetErrorMessage.restype = ctypes.c_int

        # create buffer for message
        error_message_buffer = ctypes.create_string_buffer(NamsimWrapper.MAX_BUFFER_LENGTH*2 + 1)
        call_error_code = NamsimWrapper._handler.GetErrorMessage(error_code, error_message_buffer)

        # decode error message
        error_message = NamsimWrapper._decode_buffer(error_message_buffer)

        return call_error_code, error_message


