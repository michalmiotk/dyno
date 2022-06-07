import pandas as pd

from df_from_uart import df_from_uart_rows


def test_df_from_uart_rows():
    result = df_from_uart_rows([[1, 2], [3, 4]])
    expected = pd.DataFrame({"shaft_rpm": [1, 3], "shaft_torque": [2, 4]})
    assert result.equals(expected)
