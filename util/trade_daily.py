import configparser
import eland as ed
import time

from random import randrange

from lib.browser import Driver, fetchTable
from lib.button import Btn
from lib.elastic import ESClient
from lib.selector import Selector, Dates

def TradeDaily(cfg: configparser.ConfigParser):
    # Get and setup browser driver
    driver = Driver()
    driver.implicitly_wait(2)
    try:
        driver.get(cfg["trade_daily"])
    except Exception as err:
        raise err

    # Location of date selectors and search button
    selectors = [Selector(driver, "yy"), Selector(driver, "mm")]
    search = Btn(driver, "//form[@class='main']//a[@class='button search']")
    # Check from database for fetch begining date
    dates = Dates(selectors, cfg["trade_daily_index_name"], "Date")

    for date in dates:
        selectors[0].select_by_value(str(date["y"]))
        selectors[1].select_by_value(str(date["m"]))
        search.click()

        table = fetchTable(driver)
        df = table[0]
        df["Date"] = df["Date"].str.replace("/", "-")
        df.set_index("Date", inplace=True, drop=False)

        # Insert to elasticsearch
        ed.pandas_to_eland(
            pd_df=df,
            es_client=ESClient(),
            es_dest_index=cfg["trade_daily_index_name"],
            es_if_exists="append",
            es_refresh=True,
            es_type_overrides={
                "Date": "date"
            }
        )
        # Random pause to avoid IP block
        time.sleep(randrange(2, int(cfg['action_interval_seed'])))

    driver.quit()