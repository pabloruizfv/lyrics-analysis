from os.path import join, exists
from os import mkdir


def string_for_path(text):
    """
    Given some text, modify it so that it can be used as a part of a Windows
    path.
    :param text: (string)
    :return text: (string)
    """
    characters_to_replace_by_underscore = ['/', '\\', '|', ':', ' ', '.', '\n']
    for ch in characters_to_replace_by_underscore:
        text = text.replace(ch, '_')

    characters_to_discard = ['<', '>', '\"', '*', '?']
    for ch in characters_to_discard:
        text = text.replace(ch, '')

    return text


def create_subdir(directory, subdir_name):
    """
    Checks if a directory under "subdir_name" exists under a given directory.
    If not, it creates it. Returns the full path to the subdirectory.
    :param directory: (string) path to the parent directory.
    :param subdir_name: (string) name of the directory to generate.
    :return subdir: (string) full path to the new subdirectory.
    """
    subdir = join(directory, subdir_name)
    if not exists(subdir):
        mkdir(subdir)
    return subdir
