import os
import sys
from rich.console import Console
from rich.theme import Theme


class ClearConsole:
    @staticmethod
    def clear_console():
        """
        Clears the console.
        Code taken from https://www.delftstack.com/howto/python/python-clear-console/
        """
        return os.system("cls" if os.name in ("nt", "dos") else "clear")


class StyleConsole:
    @staticmethod
    def style():
        """
        Creates a custom theme to use with the rich package

        :return: Console with custom theme
        """
        custom_theme = Theme({
            "error": "bold red",
            "heading": "bold underline",
            "option": "bold",
            "info": "dim",
            "success": "bold green",
            "center_heading": "bold white on green"
        })

        return Console(theme=custom_theme)


class RestartProgram:
    @staticmethod
    def restart():
        """
        Restart the program.
        Code taken from https://bobbyhadz.com/blog/how-to-restart-python-script-from-within-itself
        """
        os.execv(sys.executable, ['python'] + sys.argv)
