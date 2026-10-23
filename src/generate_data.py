import os
import pandas as pd
import numpy as np

def generate_telecom_telemetry(n_sites: int = 50, days: int = 30) -> pd.DataFrame:
    np.random.seed(42)  # For reproducibility
    n_hours = 24 * days
    site_ids = [f"SITE_{str(i).zfill(3)}" for i in range(1, n_sites + 1)]
    timestamps = pd.date_range(start='2026-01-01', periods=n_hours, freq='h')

    data = []
    print(f"Generating telemetry data for {n_sites} sites over {days} days...")

    for site in site_ids:
        base_traffic = np.random.uniform(50,200)  # Base traffic in Mbps
        base_temp = np.random.uniform(35,55)  # Base temperature in Celsius

        for ts in timestamps:
            hour_factor = np.sin(ts.hour * np.pi / 12) # Simulate daily traffic pattern
            traffic = max(5.0, base_traffic + hour_factor * 30) +np.random.normal(0,15)  # Add noise
            temp = base_temp + (hour_factor *8) + np.random.normal(0,3)  # Add noise


            if temp > 65:
                packet_loss = max (0.0, np.random.exponential(8.0))  # Simulate packet loss for high temperatures
            else:
                packet_loss = max(0.0, np.random.exponential(1.5))  # Normal packet loss

            rssi = np.random.uniform(-75, 5)  # Random RSSI value in dBm
            failure_logit = 0.0 * (temp - 60) + 0.2 * (packet_loss - 5) 
            failure_prob = 1 / (1 + np.exp(-failure_logit))
            failure = 1 if np.random.rand() < failure_prob else 0
            data.append({
                "site_id": site,
                "timestamp": ts,
                "traffic_volume_gb": round(traffic, 2),
                "packet_loss_rate": round(packet_loss, 2),
                "temperature_c": round(temp, 2),
                "rssi_dbm": round(rssi, 2), 
                "target_failure": failure
            })
    return pd.DataFrame(data)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    telemetry_df = generate_telecom_telemetry(n_sites=50, days=30)        
    output_path = os.path.join("data", "telecom_site_logs.csv")
    telemetry_df.to_csv(output_path, index=False)
    print (f"Telemetry data generated and saved successfully to '{output_path}'.")   

    # python src/generate_data.py
