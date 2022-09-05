import unittest

from token_original_id.token_original_id_table import TokenOriginalIdTable


class TestTokenOriginalIdTable(unittest.TestCase):
    def test_get_all_meta_data(self):
        token_original_id_table = TokenOriginalIdTable()
        metadata = token_original_id_table.get_all_meta_data(
            "osmosis",
            "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2",
        )
        if metadata is None:
            assert False
        assert metadata["uti"] == "atom"
        assert metadata["platform"] == "osmosis"
        assert (
            metadata["original_id"]
            == "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"
        )

        metadata = token_original_id_table.get_all_meta_data(
            "osmosis",
            "ibc/27394FB092D2ECCD56123C74F36e4C1F926001CEADA9CA97EA622b25F41E5EB2",
        )
        if metadata is None:
            assert False
        assert metadata["uti"] == "atom"
        assert metadata["platform"] == "osmosis"
        assert (
            metadata["original_id"]
            == "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"
        )

    def test_get_uti_exist(self):
        token_original_id_table = TokenOriginalIdTable()
        uti = token_original_id_table.get_uti(
            "osmosis",
            "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2",
        )
        assert uti == "atom"

    def test_get_uti_nonexist_no_default_symbol(self):
        token_original_id_table = TokenOriginalIdTable()
        uti = token_original_id_table.get_uti(
            "osmosis",
            "gamm/pool/497",
        )
        assert uti == "gamm%2Fpool%2F497"

    def test_get_uti_nonexist_with_default_symbol(self):
        token_original_id_table = TokenOriginalIdTable()
        uti = token_original_id_table.get_uti(
            "osmosis",
            "ibc/noexist",
            "atomm",
        )
        assert uti == "atomm/ibc%2Fnoexist"

    def test_get_symbol(self):
        token_original_id_table = TokenOriginalIdTable()
        symbol = token_original_id_table.get_symbol(
            "osmosis",
            "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2",
        )
        assert symbol == "atom"
