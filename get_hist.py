from binance_historical_data import BinanceDataDumper

data_dumper = BinanceDataDumper(
    path_dir_where_to_dump="data",
    asset_class="spot",
    data_type="klines",
    data_frequency="1m"
)
data_dumper.dump_data()