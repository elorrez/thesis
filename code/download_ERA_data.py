from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()
server.retrieve({
    "class": "ei",
    "dataset": "interim",
    "date": "/".join([f"{2000 + year}{month:02}01" for year in range(19) for month in range(1,13)]),
    "expver": "1",
    "grid": "1/1",
    "levtype": "sfc",
    "param": "176.128",
    "step": "12",
    "stream": "mnth",
    "time": "12:00:00",
    "type": "fc",
    "target": "ERA_data.nc",
    'area': "10/0/-10/40"
})