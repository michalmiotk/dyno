from typing import List
import pandas as pd

def df_from_uart_row(uart_row: List):
    return pd.DataFrame({'shaft_rpm': [uart_row[0]], 'shaft_torque_Nm': [uart_row[1]]})
