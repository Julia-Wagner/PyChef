import os
from rich.console import Console
from rich.theme import Theme


class ClearConsole:
    @staticmethod
    def clear_console():
        """
        Clear the console
        Code taken from https://www.delftstack.com/howto/python/python-clear-console/
        :return:
        """
        return os.system("cls" if os.name in ("nt", "dos") else "clear")


class StyleConsole:
    @staticmethod
    def style():
        custom_theme = Theme({
            "error": "bold red",
            "heading": "bold underline",
            "option": "bold",
            "info": "dim",
            "success": "bold green"
        })

        return Console(theme=custom_theme)
