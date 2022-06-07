def raw_serial_row_to_filtered_data(serial_data):
    serial_data = serial_data.decode("UTF-8")
    serial_data = serial_data.strip("\n").strip("\r")
    filter_data = serial_data.split(",")
    filter_data = [int(d) for d in filter_data]
    return filter_data
