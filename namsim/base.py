from namsim.wrapper.wrapper_imp import NamsimWrapper


class Namsim(object):
    MAX_INSTANCES = 64
    _free_ids_list = list(reversed([i for i in range(MAX_INSTANCES)]))

    @staticmethod
    def _validate_error_code(error_code, on_failure=None):
        if error_code != 0:
            if on_failure is not None:
                on_failure()
            raise Exception('Internal error has occurred with error code: {}.'.format(error_code))

    def __init__(self, conf_path=None):
        if len(Namsim._free_ids_list) == 0:
            raise Exception("Number of Namsim instances exceeded the maximum {}.".format(Namsim.MAX_INSTANCES))

        # extract free id
        namsim_id = Namsim._free_ids_list.pop()

        # create instance, on failure push back the free id
        error_code = NamsimWrapper.namsim_init(namsim_id, conf_path=conf_path)
        Namsim._validate_error_code(error_code, on_failure=lambda: Namsim._free_ids_list.append(namsim_id))

        self._id = namsim_id

    def similarity(self, word1, word2):
        error_code, sim = NamsimWrapper.namsim_similarity(self._id, word1, word2)
        Namsim._validate_error_code(error_code)

        return sim

    def __exit__(self, exc_type, exc_val, exc_tb):
        error_code = NamsimWrapper.namsim_done(self._id)
        Namsim._validate_error_code(error_code)

        # add id to free list
        Namsim._free_ids_list.append(self._id)



