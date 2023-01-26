import configparser

from util.taiex import TAIEX
from util.trade_daily import TradeDaily

def Stock(cfg: configparser.ConfigParser):
    # TAIEX(cfg)
    TradeDaily(cfg)
