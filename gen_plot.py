import argparse
import json
import matplotlib.pyplot as plt
import os
import pandas as pd

from datetime import datetime

def parse_json_safe(s):
    try:
        return json.loads(s)
    except:
        return {}

def gen_plot(df, keyword, output_file):
    if df.empty:
        print("Empty DataFrame")
        return

    # Flatten the entire 'data_parsed' column at once
    # This creates a DataFrame where each column is sensor_name.keyword or sensor_name.timestamp
    normalized = pd.json_normalize(df['data_parsed'])

    # Filter only columns that contain the keyword
    value_cols = [col for col in normalized.columns if col.endswith(f".{keyword}")]
    if not value_cols:
        print(f"No measurements found for keyword '{keyword}'")
        return

    # Extract timestamps vectorized
    ts_cols = [col for col in normalized.columns if col.endswith(".timestamp")]
    if not ts_cols:
        print("No timestamps found")
        return

    # Melt DataFrame to long format
    # value_cols contain the sensor readings
    long_df = normalized.melt(value_vars=value_cols, var_name='sensor', value_name='value')

    # Extract sensor name from column name
    long_df['sensor'] = long_df['sensor'].str.replace(f".{keyword}", "", regex=False)

    # Repeat timestamps for each sensor value
    # For simplicity, take the first timestamp column (assuming all sensors in a row have same timestamp)
    timestamps = pd.to_datetime(normalized[ts_cols[0]])
    long_df['timestamp'] = pd.concat([timestamps]*len(value_cols), ignore_index=True)

    # Plot using explicit figure
    fig, ax = plt.subplots(figsize=(10, 6))

    for sensor, sensor_data in long_df.groupby("sensor"):
        ax.plot(sensor_data["timestamp"], sensor_data["value"], label=sensor)

    ax.set_xlabel("Time")
    ax.set_ylabel(keyword.capitalize())
    ax.set_title(keyword.capitalize())
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    # Save plot
    plt_dir = "plots"
    os.makedirs(plt_dir, exist_ok=True)
    plt.show()
    fig.savefig(output_file)

    plt.close(fig)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Plot measurements results from CSV datafile")
    parser.add_argument("filename", help="Path to CSV datafile")
    parser.add_argument("-t", "--temperature", action="store_true", help="Plot temperature")
    parser.add_argument("-hu", "--humidity", action="store_true", help="Plot humidity")
    parser.add_argument("-p", "--pressure", action="store_true", help="Plot pressure")
    parser.add_argument("-m", "--moisture", action="store_true", help="Plot moisture")
    parser.add_argument("-o", "--output", help="Optional output filename prefix for plots, otherwise will be saved under the same name as input file") 
    args = parser.parse_args()

    plot_dir = "plots"
    os.makedirs(plot_dir, exist_ok = True)    

    if args.output:
        output_prefix = args.output
    else:
        output_prefix = os.path.splitext(os.path.basename(args.filename))[0]

    df = pd.read_csv(args.filename)    
    df['data_parsed'] = df['data'].apply(parse_json_safe)

    plots = {
        "temperature": args.temperature,
        "humidity": args.humidity,
        "pressure": args.pressure,
        "moisture": args.moisture,
    }

    for keyword, enabled in plots.items():
        if enabled:
            gen_plot(df, keyword, os.path.join(plot_dir, f"{output_prefix}_{keyword}.png"))

    
