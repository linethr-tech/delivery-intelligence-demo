import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Delivery Intelligence Demo
# Business-specific anomaly detection example
# ---------------------------------------------------------

# Load synthetic delivery data
df = pd.read_csv("data/deliveries.csv")

# Calculate delivery delay
df["delay_days"] = (
    df["actual_delivery_days"] - df["planned_delivery_days"]
)

# Build a simple anomaly detection model
model = IsolationForest(
    contamination=0.20,
    random_state=42
)

# Detect unusual delivery behaviour
df["anomaly"] = model.fit_predict(
    df[["delay_days"]]
)

# Convert model output into business-friendly labels
df["status"] = df["anomaly"].map({
    1: "Normal",
    -1: "Potential anomaly"
})

# Display results
print("\nDELIVERY INTELLIGENCE - ANOMALY DETECTION\n")

print(
    df[
        [
            "delivery_id",
            "customer",
            "country",
            "carrier",
            "planned_delivery_days",
            "actual_delivery_days",
            "delay_days",
            "status"
        ]
    ].to_string(index=False)
)

# Focus attention on anomalous deliveries
anomalies = df[df["anomaly"] == -1]

print("\nPotential delivery anomalies requiring investigation:\n")

print(
    anomalies[
        [
            "delivery_id",
            "customer",
            "country",
            "carrier",
            "delay_days"
        ]
    ].to_string(index=False)
)
# --------------------------------------------------
# Visualize detected delivery anomalies
# --------------------------------------------------

plt.figure(figsize=(10, 6))

normal = df[df["anomaly"] == 1]
anomalies = df[df["anomaly"] == -1]

plt.scatter(
    normal["planned_delivery_days"],
    normal["delay_days"],
    color="steelblue",
    label="Normal deliveries",
    alpha=0.7
)

plt.scatter(
    anomalies["planned_delivery_days"],
    anomalies["delay_days"],
    color="red",
    label="Detected anomalies",
    s=80
)

plt.axhline(
    y=0,
    color="gray",
    linestyle="--",
    linewidth=1
)

plt.xlabel("Planned Delivery Days")
plt.ylabel("Delivery Delay (Days)")
plt.title("Delivery Intelligence - Anomaly Detection")

plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig("delivery_anomalies.png", dpi=150)

plt.show()
