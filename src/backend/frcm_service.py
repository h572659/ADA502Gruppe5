def calculate_fire_risk(met_json: dict):
    # TODO: Replace with real FRCM library call
    # For now just extract values to show the pipeline works
    details = met_json["properties"]["timeseries"][0]["data"]["instant"]["details"]
    return {
        "air_temperature": details.get("air_temperature"),
        "wind_speed": details.get("wind_speed"),
        "relative_humidity": details.get("relative_humidity"),
    }
### må spørre på fredag eller i morgen om har har fått selve FRCM koden / biblioteket fra 
###  kurset, eller det jeg har gjørt er nok.
