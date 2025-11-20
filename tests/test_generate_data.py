import datetime

import pandas as pd

from generate_data import generate_prices, MATERIALS_CONFIG


def test_generate_prices_shape_and_columns():
    # small date range for quick test
    start = datetime.date(2025, 1, 1)
    end = datetime.date(2025, 1, 3)
    df = generate_prices(start_date=start, end_date=end,
                         materials_config=MATERIALS_CONFIG, seed=123)

    # Expect 3 days * number of materials rows
    expected_rows = 3 * len(MATERIALS_CONFIG)
    assert len(df) == expected_rows

    # Required columns
    required = {'Date', 'Material', 'Unit', 'Price_INR', '7_Day_Avg'}
    assert required.issubset(set(df.columns))

    # Check types
    assert pd.api.types.is_float_dtype(
        df['Price_INR']) or pd.api.types.is_integer_dtype(df['Price_INR'])
    assert pd.api.types.is_float_dtype(
        df['7_Day_Avg']) or pd.api.types.is_integer_dtype(df['7_Day_Avg'])
