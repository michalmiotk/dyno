from uart_preprocessing import convert_raw_serial_row_to_filtered_data

def test_convert_raw_serial_row_to_filtered_data():
    assert convert_raw_serial_row_to_filtered_data(b'8, 2500\r\n') == [8, 2500]