# temperature_analysis.py
# in the terminal type pip install pandas if pandas is not installed
import pandas as pd
from pathlib import Path

# ------------------ helpers ------------------

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def load_all_data(folder="temperatures"):
    """Load all CSVs and reshape to long format: Station, Month, Temperature."""
    folder_path = Path(folder)
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path.resolve()}")

    all_files = list(folder_path.glob("*.csv"))
    if not all_files:
        raise FileNotFoundError("No CSV files found in the temperatures folder.")

    dfs = []
    for file in all_files:
        df = pd.read_csv(file)

        # Check required columns
        if not {"STATION_NAME", "STN_ID"}.issubset(df.columns):
            raise ValueError(f"Missing required station columns in {file.name}")

        # Melt months into rows
        df_long = df.melt(
            id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
            value_vars=MONTHS,
            var_name="Month",
            value_name="Temperature"
        )
        dfs.append(df_long)

    return pd.concat(dfs, ignore_index=True)

def assign_season(month: str):
    """Return Australian season given month name."""
    if month in ["December", "January", "February"]:
        return "Summer"
    elif month in ["March", "April", "May"]:
        return "Autumn"
    elif month in ["June", "July", "August"]:
        return "Winter"
    elif month in ["September", "October", "November"]:
        return "Spring"
    return None

# ------------------ analysis functions ------------------

def seasonal_average(df: pd.DataFrame, out_file="average_temp.txt"):
    df = df.dropna(subset=["Temperature"])
    df["Season"] = df["Month"].map(assign_season)

    results = df.groupby("Season")["Temperature"].mean().round(1)

    lines = [f"{season}: {temp:.1f}°C" for season, temp in results.items()]
    Path(out_file).write_text("\n".join(lines), encoding="utf-8")

def largest_temp_range(df: pd.DataFrame, out_file="largest_temp_range_station.txt"):
    df = df.dropna(subset=["Temperature"])
    grouped = df.groupby("STATION_NAME")["Temperature"]

    stats = grouped.agg(["min", "max"])
    stats["range"] = stats["max"] - stats["min"]

    max_range = stats["range"].max()
    top = stats[stats["range"] == max_range]

    lines = [
        f"{station}: Range {row['range']:.1f}°C (Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)"
        for station, row in top.iterrows()
    ]
    Path(out_file).write_text("\n".join(lines), encoding="utf-8")

def temperature_stability(df: pd.DataFrame, out_file="temperature_stability_stations.txt"):
    df = df.dropna(subset=["Temperature"])
    grouped = df.groupby("STATION_NAME")["Temperature"]

    stds = grouped.std()
    min_std = stds.min()
    max_std = stds.max()

    most_stable = stds[stds == min_std]
    most_variable = stds[stds == max_std]

    lines = []
    for station, val in most_stable.items():
        lines.append(f"Most Stable: {station}: StdDev {val:.1f}°C")
    for station, val in most_variable.items():
        lines.append(f"Most Variable: {station}: StdDev {val:.1f}°C")

    Path(out_file).write_text("\n".join(lines), encoding="utf-8")

# ------------------ main ------------------

if __name__ == "__main__":
    df = load_all_data("temperatures")

    seasonal_average(df)
    largest_temp_range(df)
    temperature_stability(df)

    print("Analysis complete. Results saved to:")
    print("  - average_temp.txt")
    print("  - largest_temp_range_station.txt")
    print("  - temperature_stability_stations.txt")
