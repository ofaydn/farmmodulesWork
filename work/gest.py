def get_measurement(self):
    """Function to get the measurements from the sensor"""
    measurements = fetch_meausrements(measurementsApiUrl)
    if measurements:
        print("Measurements fetched succesfully.")
    else:
        print("Measurements couldn't fetched.")
    self.return_dict = copy.deepcopy(measurements_dict)
    try:
        temperature_c = get_measurements