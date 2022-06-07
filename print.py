import win32api


def print_file(file_to_print):
    win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)
