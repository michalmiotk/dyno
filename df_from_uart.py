from typing import List
import pandas as pd

def df_from_uart_rows(uart_rows: List[List]):
    return pd.DataFrame({'shaft_rpm': [uart_row[0] for uart_row in uart_rows], 'shaft_torque_Nm': [uart_row[1] for uart_row in uart_rows]})
    