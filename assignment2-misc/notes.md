# Notes

deployment

- Where are the nodes in the room, how do we reduce chance of nodes being stolen
- Consider time. How long are nodes going to be deployed, and what does it mean for the power budget?

Investigate

- Difference between nodes in different parts of the room
- Is CO2 level above the legal limits?
- Does CO2 level correlate with when the room is scheduled on timeedit

Battery specs

- 2 ah
- 3.7 v

Power consumption Pycom (@ 5v)

- idle: 35.4 mA
- Lora transmit: 108 mA
- Deep sleep: 18.5 microA
- [datasheet](https://cdn.sparkfun.com/assets/e/b/2/9/0/lopy4-specsheet.pdf)

Power consumption SDC30 (@ 3.3v)

- average with 2 s read interval: 19 mA
- during measurement: 75 mA
- [datasheet](https://sensirion.com/media/documents/4EAF6AF8/61652C3C/Sensirion_CO2_Sensors_SCD30_Datasheet.pdf)
