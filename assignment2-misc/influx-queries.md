# Queries

To get CO2 reading from a reading (for some reason rounds floats)

```influxql
import "regexp"
regex = /\d+\.\d+/


from(bucket: "iot2023")
  |> range(start: v.timeRangeStart, stop:v.timeRangeStop)
  |> filter(fn: (r) =>
    r._measurement == "tjoms_measurement" and
    r._field == "payload_decoded" and
    r.device_id == "eui-808abcdef0abcdef"
  )
  |> map(fn: (r) => ({r with _value: float(v: regexp.findString(v: r._value, r: regex))}))
```
