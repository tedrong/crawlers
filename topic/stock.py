import configparser

from util.taiex import TAIEX

def Stock(cfg: configparser.ConfigParser):
    TAIEX(cfg)
