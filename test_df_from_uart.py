import pandas as pd
from pandas.testing import assert_frame_equal

from df_from_uart import df_from_uart_rows

def test_df_from_uart_rows():
    result = df_from_uart_rows([[1, 2], [3, 4]])
    assert result.equals(pd.DataFrame({'shaft_rpm': [1,3], 'shaft_torque_Nm': [2,4]}))
