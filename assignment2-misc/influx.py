import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import base64

bucket = "iot2023"
org = "iot2023"
token = "JfgEuZ1g80KzI6U6LR8jnQ9Ol6yXe7Q-gTV74ConWb6VJLyPQRKlVMd4e6QrfoiN1LKI2NnEPAMF_C0MhASuUQ=="
url="http://influx.itu.dk:8086/"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

# Query script
query_api = client.query_api()
query = f'from(bucket:"{bucket}")\
|> range(start: -10d)\
|> filter(fn: (r) => r.dev_eui == "804ABCDEF0ABCDEF")'
result = query_api.query(org=org, query=query)
for table in result:
    for record in table.records:
        print(record)
        point = influxdb_client.Point("tjoms_measurement") \
        .tag("device_id",record.values.get("device_id")) \
        .field("payload_decoded", base64.b64decode(record.get_value()).decode("ISO-8859-1")) \
        .time(record.get_time())
        print(point)
        write_api.write(bucket, org, point)