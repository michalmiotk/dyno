import pandas as pd
from pandas.testing import assert_frame_equal

from df_from_uart import df_from_uart_row

def test_df_from_uart_row():
    result = df_from_uart_row([1, 2])
    assert result.equals(pd.DataFrame({'shaft_rpm': [1], 'shaft_torque_Nm': [2]}))
