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

def gen_plot(df, keyword):
    rows = []
    
    for idx, row in df.iterrows():
      #  print(f"IDX: {idx}")
      #  print(f"row: {row}")

        for sensor_name, sensor_data in row["data_parsed"].items():
            if keyword in sensor_data:
                timestamp = pd.to_datetime(sensor_data["timestamp"])
                value = sensor_data[keyword]

                rows.append({"sensor": sensor_name, "timestamp": timestamp, "value": value})

    if not rows:
        print("No measurements found")
        exit(0)

    plot_df = pd.DataFrame(rows)
    plt.figure(figsize=(10,6))

    for sensor in plot_df["sensor"].unique():
        sensor_data = plot_df[plot_df["sensor"] == sensor]
        plt.plot(sensor_data["timestamp"], sensor_data["value"], marker="o", label=sensor)

    plt.xlabel("Time")
    plt.ylabel(keyword.capitalize())
    plt.title(f"{keyword.capitalize()} measurements over time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig(os.path.join("plots", keyword + ".png"))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Plot measurements results from CSV datafile")
    parser.add_argument("filename", help="Path to CSV datafile")
    parser.add_argument("-t", "--temperature", action="store_true", help="Plot temperature")
    parser.add_argument("-hu", "--humidity", action="store_true", help="Plot humidity")
    parser.add_argument("-p", "--pressure", action="store_true", help="Plot pressure")
    parser.add_argument("-m", "--moisture", action="store_true", help="Plot moisture")
    args = parser.parse_args()

    df = pd.read_csv(args.filename)    
    df['data_parsed'] = df['data'].apply(parse_json_safe)

    if args.temperature:
        gen_plot(df, "temperature")
    if args.humidity:
        gen_plot(df, "humidity")
    if args.pressure:
        gen_plot(df, "pressure")
    if args.moisture:
        gen_plot(df, "moisture")    

    #else:
    #   print("ERROR: No valid measurement chosen")
        exit()

    
