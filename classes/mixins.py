import os


class ClearConsole:
    @staticmethod
    def clear_console():
        """
        Clear the console
        Code taken from https://www.delftstack.com/howto/python/python-clear-console/
        :return:
        """
        return os.system("cls" if os.name in ("nt", "dos") else "clear")
