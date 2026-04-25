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

def load_data(filename, topic_filter=None):
    data_list = []

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            entry = parse_json_safe(line)
            if not entry:
                continue

            # Filter by topic if requested
            if topic_filter and entry.get("topic") != topic_filter:
                continue

            data_list.append(entry)

    if not data_list:
        print("No data to plot")
        return None

    df = pd.DataFrame(data_list)
    df['data_parsed'] = df['data']

    # Flatten the 'data' column 
    normalized = pd.json_normalize(df['data_parsed'])

    return normalized

def gen_plot(data, keyword, output_file):
    if data.empty:
        print("Empty DataFrame")
        return

    # Filter columns by keyword
    value_cols = [col for col in data.columns if col.endswith(f".{keyword}")]
    if not value_cols:
        print(f"No measurements found for keyword '{keyword}'")
        return
  
    fig, ax = plt.subplots(figsize=(10, 6))

    for col in value_cols:
        sensor = col.replace(f".{keyword}", "")
        ts_col = f"{sensor}.timestamp"

        if ts_col not in data.columns:
            continue

        values = data[col]
        timestamps = pd.to_datetime(data[ts_col], errors="coerce")

        # Drop NaNs to avoid empty plots
        mask = values.notna() & timestamps.notna()
        values = values[mask]
        timestamps = timestamps[mask]

        if not values.empty:
            ax.plot(timestamps, values, label=sensor)

    ax.set_xlabel("Time")
    ax.set_ylabel(keyword.capitalize())
    ax.set_title(keyword.capitalize())
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    # Save plot
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
    parser.add_argument("--topic", help="Optional topic filter to plot only specific MQTT topic")
    args = parser.parse_args()

    output_prefix = args.output if args.output else os.path.splitext(os.path.basename(args.filename))[0]
    plot_dir = "plots"
    os.makedirs(plot_dir, exist_ok=True)

    data = load_data(args.filename, args.topic)
    if data is None:
        exit(0)

    plots = {
        "temperature": args.temperature,
        "humidity": args.humidity,
        "pressure": args.pressure,
        "moisture": args.moisture,
    }

    for keyword, enabled in plots.items():
        if enabled:
            gen_plot(data, keyword, os.path.join(plot_dir, f"{output_prefix}_{keyword}.png"))

    
