"""generate_data.py

Small utility to synthesize daily construction material prices
for demonstration and testing purposes.

Usage:
    python generate_data.py --output construction_material_prices.csv

The script is deterministic by default (seed=42) but accepts a
`--seed` argument to vary the random noise.
"""

from pathlib import Path
import argparse
import datetime
import numpy as np
import pandas as pd
from typing import Dict, Any


MATERIALS_CONFIG: Dict[str, Dict[str, Any]] = {
    'Cement (OPC 53 Grade)': {'base': 380.0, 'volatility': 10.0, 'unit': 'Per 50kg Bag'},
    'Steel (TMT Fe550)': {'base': 58000.0, 'volatility': 1000.0, 'unit': 'Per Ton'},
    'River Sand': {'base': 1600.0, 'volatility': 70.0, 'unit': 'Per Cubic Meter'},
    'Aggregates (20mm)': {'base': 1300.0, 'volatility': 60.0, 'unit': 'Per Cubic Meter'}
}


def generate_prices(start_date: datetime.date,
                    end_date: datetime.date,
                    materials_config: Dict[str, Dict[str, Any]],
                    seed: int = 42) -> pd.DataFrame:
    """Generate a DataFrame containing daily prices for materials.

    Args:
        start_date: inclusive start date
        end_date: inclusive end date
        materials_config: mapping of material -> config
        seed: random seed for reproducibility

    Returns:
        pd.DataFrame with columns: Date, Material, Unit, Price_INR, 7_Day_Avg
    """
    rng = pd.date_range(start=start_date, end=end_date, freq='D')
    np.random.seed(seed)
    rows = []

    for date in rng:
        for material, cfg in materials_config.items():
            base = float(cfg['base'])
            vol = float(cfg['volatility'])
            seasonal = 0.05 * \
                np.sin(2 * np.pi * (date.dayofyear - 80) / 365.25)
            noise = np.random.normal(0, vol / 3)
            price = base + (base * seasonal) + noise

            # Example one-off event: steel jump on Feb 5
            if date.month == 2 and date.day == 5 and 'Steel' in material:
                price *= 1.15

            rows.append((pd.Timestamp(date).date(), material,
                        cfg['unit'], round(price, 2)))

    df = pd.DataFrame(rows, columns=['Date', 'Material', 'Unit', 'Price_INR'])
    df['7_Day_Avg'] = df.groupby('Material')['Price_INR'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    ).round(2)
    return df


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description='Generate synthetic construction prices CSV')
    p.add_argument('--output', '-o', type=Path, default=Path('construction_material_prices.csv'),
                   help='Output CSV filename')
    p.add_argument('--days', '-d', type=int, default=365,
                   help='Number of days of history (ending last day of previous month)')
    p.add_argument('--seed', type=int, default=42, help='Random seed')
    return p.parse_args()


def main() -> int:
    args = parse_args()

    # end_date: last day of previous month
    today = datetime.date.today()
    last_day_prev_month = today.replace(day=1) - datetime.timedelta(days=1)
    start_date = last_day_prev_month - datetime.timedelta(days=args.days - 1)

    try:
        df = generate_prices(start_date=start_date, end_date=last_day_prev_month,
                             materials_config=MATERIALS_CONFIG, seed=args.seed)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.output, index=False)
        print(
            f"Generated {len(df)} rows and saved to: {args.output.resolve()}")
        return 0
    except Exception as exc:  # pragma: no cover - surface-level error handling
        print(f"Error generating data: {exc}")
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
