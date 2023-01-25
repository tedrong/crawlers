import configparser
import eland as ed
import pandas as pd
import time

from random import randrange
from selenium import webdriver

from lib.browser import Driver
from lib.button import Btn
from lib.elastic import ESClient
from lib.selector import Selector, Dates

def TAIEX(cfg: configparser.ConfigParser):
    # Get and setup browser driver
    driver = Driver()
    driver.implicitly_wait(2)
    try:
        driver.get(cfg['taiex'])
    except Exception as err:
        raise err

    # Location of date selectors and search button
    selectors = [Selector(driver, "yy"), Selector(driver, "mm")]
    search = Btn(driver, "//form[@class='main']//a[@class='button search']")
    # Check from database for fetch begining date
    dates = Dates(selectors, "stock_taiex", "Date")

    for date in dates:
        selectors[0].select_by_value(str(date["y"]))
        selectors[1].select_by_value(str(date["m"]))
        search.click()

        table = fetchTable(driver)
        df = table[0]
        df["Date"] = df["Date"].str.replace("/", "-")
        df.set_index("Date", inplace=True, drop=False)
        ed.pandas_to_eland(
            pd_df=df,
            es_client=ESClient(),
            es_dest_index="stock_taiex",
            es_if_exists="append",
            es_refresh=True,
            es_type_overrides={
                "Date": "date"
            }
        )
        time.sleep(randrange(2, int(cfg['action_interval_seed'])))
    driver.quit()

def fetchTable(driver: webdriver):
    retry = 2
    while True:
        if retry > 16:
            return None
        try:
            return pd.read_html(driver.page_source)
        except:
            time.sleep(retry)
            retry *= 2