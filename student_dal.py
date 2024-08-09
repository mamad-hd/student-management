from os.path import isfile
from typing import Iterable


def save_data(path: str, data: str, mode: str = "a"):
    function_result = {
        "SUCCESS": True,
        "ERROR_MESSAGE": {},
        "SUCCESS_MESSAGE": {},
        "RETURN_DATA": None
    }

    file_object = None

    try:
        file_object = open(file=path, mode=mode)
        file_object.write(data)
    except BaseException as err:
        function_result["SUCCESS"] = False
        function_result["ERROR_MESSAGE"]["DALERROR"] = "file error!!!"
        function_result["RETURN_DATA"] = err
        return function_result
    else:
        return function_result
    finally:
        if file_object and (not file_object.closed):
            file_object.close()


def save_iter_data(path: str, data: Iterable[str], mode: str = "a"):
    function_result = {
        "SUCCESS": True,
        "ERROR_MESSAGE": {},
        "SUCCESS_MESSAGE": {},
        "RETURN_DATA": None
    }

    file_object = None

    try:
        file_object = open(file=path, mode=mode)
        file_object.writelines(data)
    except BaseException as err:
        function_result["SUCCESS"] = False
        function_result["ERROR_MESSAGE"]["DALERROR"] = "file error!!!"
        function_result["RETURN_DATA"] = err
        return function_result
    else:
        return function_result
    finally:
        if file_object and (not file_object.closed):
            file_object.close()


def load_data(path: str):
    function_result = {
        "SUCCESS": True,
        "ERROR_MESSAGE": {},
        "SUCCESS_MESSAGE": {},
        "RETURN_DATA": None
    }

    if not isfile(path=path):
        file_object = None

        try:
            file_object = open(file=path, mode="x")
        except BaseException as err:
            function_result["SUCCESS"] = False
            function_result["ERROR_MESSAGE"]["DALERROR"] = "file error!!!"
            function_result["RETURN_DATA"] = err
            return function_result
        else:
            function_result["RETURN_DATA"] = []
            return function_result
        finally:
            if file_object and (not file_object.closed):
                file_object.close()



    file_object = None

    try:
        file_object = open(file=path)
        res = file_object.readlines()
    except BaseException as err:
        function_result["SUCCESS"] = False
        function_result["ERROR_MESSAGE"]["DALERROR"] = "file error!!!"
        function_result["RETURN_DATA"] = err
        return function_result
    else:
        function_result["RETURN_DATA"] = res
        return function_result
    finally:
        if file_object and (not file_object.closed):
            file_object.close()