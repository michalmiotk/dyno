def convert_raw_serial_row_to_filtered_data(serial_data):
    serial_data = serial_data.decode("UTF-8")
    print("oooo", serial_data)
    serial_data = serial_data.strip('\n').strip('\r')
    print(serial_data)
    filter_data = serial_data.split(',')
    filter_data = [int(d) for d in filter_data]
    return filter_data