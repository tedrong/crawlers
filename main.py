import configparser
import sys

from lib.elastic import ESInit
from topic.stock import Stock

if __name__ == "__main__":
    # Reading config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    # Init elasticsearch database password
    ESInit(config['elastic'])
    # Exit and show error cause by argument number incorrect
    if len(sys.argv) <= 1:
        print("Wrong argument number.")
        sys.exit()

    ################################
    # Functions
    ################################

    # topic = sys.argv[1:]
    topic = sys.argv[1]
    if topic == "stock":
        Stock(config['stock'])
