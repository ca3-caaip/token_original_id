from sqlite3 import Time
from sys import api_version
from pycoingecko import CoinGeckoAPI
import pandas as pd
import time
import warnings
import requests
import json


def dataframe_difference(df1, df2, which=None):
    comparison_df = df1.merge(df2,
                              indicator=True,
                              how='outer')
    if which is None:
        diff_df = comparison_df[comparison_df['_merge'] != 'both']
    else:
        diff_df = comparison_df[comparison_df['_merge'] == which]
    return diff_df

__COINGECKO_API_URL_BASE = "https://pro-api.coingecko.com/api/v3/"
warnings.simplefilter('ignore', FutureWarning)
cg = CoinGeckoAPI(__COINGECKO_API_URL_BASE)
mini_coin_list_df = pd.read_csv("coin_list.csv", na_filter=False)
token_original_table_columns = ["uti", "platform", "original_id", "description", "primary"]
token_original_table_df = pd.DataFrame(index=[], columns=token_original_table_columns)
count = 1
timeout_coins = []
value_error_coins = []
other_errors = []
other_errorslug = []
for data in mini_coin_list_df.itertuples():
    if data.symbol == "":
        continue
    coingecko_slug = data.id
    try:
        coin_data = cg.get_coin_by_id(id=coingecko_slug, x_cg_pro_api_key="ここにAPIKEY")
    except requests.exceptions.ReadTimeout:
        print(coingecko_slug)
        timeout_coins.append(coingecko_slug)
        continue
    except ValueError:
        print("Value Error, slug: {}".format(coingecko_slug))
        value_error_coins.append(coingecko_slug)
        continue
    except Exception as e:
        print("other Exception, slug:{}".format(coingecko_slug))
        other_errors.append(e)
        other_errorslug.append(coingecko_slug)
        continue
    slug_for_uti = coin_data["id"]
    uti = "{x}/{y}".format(x=coin_data["symbol"], y=slug_for_uti)
    for platform in coin_data["platforms"]:
        if platform == "":
            original_id = coin_data["symbol"]
            primary = "TRUE"
            platform = coin_data["name"].lower()
        else:
            original_id = coin_data["platforms"][platform]
            if original_id == "":
                continue
            if platform == coin_data["asset_platform_id"]:
                primary = "TRUE"
            else:
                primary = ""
        temp_data = {"uti": uti, "platform": platform, "original_id":original_id, "description": "{x}@{y}".format(x=data.id, y=data.name), "primary": primary}
        token_original_table_df = token_original_table_df.append(temp_data, ignore_index=True)
    time.sleep(0.2)
    count = count +1
    if count % 50 == 0:
        print(count)
token_original_table_df.to_csv("original_table.csv", index=False)
result = {"timeout": timeout_coins, "value_error": value_error_coins, "other": [other_errors, other_errorslug]}
with open('result.json', 'w') as f:
    json.dump(result, f, indent=4)

