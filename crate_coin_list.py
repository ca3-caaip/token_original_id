from pycoingecko import CoinGeckoAPI
import pandas as pd


cg = CoinGeckoAPI()
coin_list = cg.get_coins_list()
coin_list_df = pd.DataFrame(coin_list)
coin_list_df.to_csv("coin_list.csv", index=False)