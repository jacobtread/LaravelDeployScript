from typing import Callable, Any
import os

from log import bad

BOOLEAN_TRUE = ['y', 'yes', '1', 't', 'true']
BOOLEAN_FALSE = ['n', 'no', '0', 'f', 'false']


class InputError(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message


def accept_input(message: str, filter_callback: Callable[[str], Any]) -> str:
    while True:
        try:
            user_input = input('    ' + message)
            filter_callback(user_input)
            return user_input
        except InputError as error:
            bad(error.message)


def accept_path(message: str) -> str:
    return accept_input(message, lambda value: Validations.folder(value))


def accept_bool(message: str) -> bool:
    return accept_input(message, lambda value: value.lower() in BOOLEAN_TRUE + BOOLEAN_FALSE).lower() in BOOLEAN_TRUE


class Validations:

    @staticmethod
    def folder(path: str):
        if not os.path.exists(path):
            raise InputError(f'Could not find the folder at "{path}".')
        if not os.path.isdir(path):
            raise InputError(f'The provided path was not a directory.')

    @staticmethod
    def all():
        return True
