from uart_preprocessing import raw_serial_row_to_filtered_data


def test_raw_serial_row_to_filtered_data():
    assert raw_serial_row_to_filtered_data(b"8, 2500\r\n") == [8, 2500]
