import csv
import urllib.parse
from typing import Union, Any
from os import path
from pathlib import Path


class TokenOriginalIdTable:
    def __init__(self):
        csv_file = Path(path.join(path.dirname(__file__), "data.csv"))
        with csv_file.open() as content:
            csv_reader = csv.DictReader(content.read().strip().splitlines())
            token_original_id_table = [row for row in csv_reader]
            self.token_original_id_table: list[dict[str, Any]] = token_original_id_table

    def get_all_meta_data(
        self,
        platform: str,
        token_original_id: str,
    ) -> Union[dict[str, Any], None]:
        object_token = list(
            filter(
                lambda x: self.__is_same_original_id(token_original_id, x)
                and x["platform"].lower() == platform.lower(),
                self.token_original_id_table,
            )
        )

        if len(object_token) == 0:
            object_token = list(
                filter(
                    lambda x: self.__is_same_original_id(token_original_id, x)
                    and "/" not in x["uti"],
                    self.token_original_id_table,
                )
            )

        token_symbol = None
        if len(object_token) >= 1:
            token_symbol = object_token[0]
        return token_symbol

    def get_uti(
        self,
        platform: str,
        token_original_id: str,
        default_symbol: Union[str, None] = None,
    ) -> str:
        meta_data = self.get_all_meta_data(platform, token_original_id)
        if meta_data is not None:
            return meta_data["uti"]
        else:
            if default_symbol is not None:
                return (
                    f"{default_symbol.lower()}/{urllib.parse.quote((token_original_id.lower() if platform != 'solana' else token_original_id), safe='')}"
                )
            else:
                return f"{urllib.parse.quote((token_original_id.lower() if platform != 'solana' else token_original_id), safe='')}"

    def get_symbol(
        self,
        platform: str,
        token_original_id: str,
    ) -> Union[str, None]:
        meta_data = self.get_all_meta_data(platform, token_original_id)
        if meta_data is not None:
            symbol = urllib.parse.unquote(meta_data["uti"].split("/")[0])
            return symbol
        else:
            return None
    
    def __is_same_original_id(
        self,
        token_original_id: str,
        token_original_id_table_row: dict[str, Any]
    ) -> bool:
        if token_original_id_table_row['platform'] == 'solana':
            return token_original_id_table_row['original_id'] == token_original_id
        else:
            return token_original_id_table_row['original_id'].lower() == token_original_id.lower()
