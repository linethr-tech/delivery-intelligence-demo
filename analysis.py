import pandas as pd
from sklearn.ensemble import IsolationForest

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
