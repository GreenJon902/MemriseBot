import pathlib
import sys
from multiprocessing import freeze_support
import os

if __name__ == '__main__':
    freeze_support()

    from misc import user_data_dir

    os.chdir(pathlib.Path(__file__).parent.absolute())
    os.environ["KIVY_HOME"] = str(os.path.join(user_data_dir, "kivy"))
    os.environ["KCFG_KIVY_LOG_NAME"] = "%y-%m-%d_%_.log"
    os.environ["KCFG_KIVY_LOG_DIR"] = "../logs"
    os.environ["KCFG_KIVY_LOG_LEVEL"] = "info"

    import kivy
    from kivy.logger import Logger

    if not os.path.exists(user_data_dir):
        os.mkdir(user_data_dir)


    from misc.config import create
    create()
    Logger.info("UserDataDir: UserDataDir at \"" + str(user_data_dir) + "\"")

    from misc.config import Config
    from misc.memriseElements import MemriseElements
    MemriseElements.setup(Config)
    Logger.info("UserDataDir: UserDataDir at \"" + str(user_data_dir) + "\"")

    from misc import *
    from Gui import *


    app = MemriseAutoApp()
    app.run()
    sys.exit()
