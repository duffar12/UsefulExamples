import pandas as pd
from influxdb import InfluxDBClient
import json


#Change login credentials and edit query to continue

influxdb_client = InfluxDBClient(
            "url",
            "8086",
            "username",
            "password",
            "data_base"
        )

query = "delete from \"poloniex\" WHERE time < '2018-12-05 15:05:03.775'"
result = influxdb_client.query(query)
data = pd.read_json(json.dumps(list(result.get_points())))
