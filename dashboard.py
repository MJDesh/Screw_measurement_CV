import pandas as pd
import matplotlib.pyplot as plt
import os

CSV_FILE = "results/measurements.csv"
OUTPUT_FOLDER = "results"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ✅ Screw Specs moved here (so dashboard can use them)
SCREW_SPECS = {
    "M6x25": {"length": 31.0, "width": 10.0},
    "M8x10": {"length": 18.0, "width": 13.0},
    "M8x16": {"length": 24.0, "width": 13.0},
}

TOLERANCE_MM = 1.0

df = pd.read_csv(CSV_FILE)
df["Length(mm)"] = pd.to_numeric(df["Length(mm)"], errors="coerce")
df["Width(mm)"] = pd.to_numeric(df["Width(mm)"], errors="coerce")

# ✅ Filter accepted measurements only for trend lines
accepted_df = df[df["Status"] == "ACCEPTED"]

# Summary stats
total = len(df)
accepted = len(accepted_df)
rejected = total - accepted
reject_rate = (rejected / total) * 100 if total > 0 else 0

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Screw QC Dashboard", fontsize=20, fontweight="bold")

# === Summary Panel ===
axes[0, 0].axis('off')
summary_text = (
    f"TOTAL SAMPLES: {total}\n"
    f"ACCEPTED: {accepted}\n"
    f"REJECTED: {rejected}\n"
    f"Reject Rate: {reject_rate:.2f}%"
)
axes[0, 0].text(0.1, 0.5, summary_text, fontsize=16, family="monospace")

# === PASS vs FAIL Bar Chart ===
df["Status"].value_counts().plot(kind="bar", ax=axes[0, 1],
                                color=["green", "red"])
axes[0, 1].set_title("QC Status Count")
axes[0, 1].grid(axis='y', linestyle='--', alpha=0.5)

# === Length Trend ===
if len(accepted_df) > 0:
    # ✅ Use screw type from accepted screws
    screw_type = accepted_df["Type"].iloc[0]
    nominal_length = SCREW_SPECS[screw_type]["length"]
    upper_tol_len = nominal_length + TOLERANCE_MM
    lower_tol_len = nominal_length - TOLERANCE_MM

    length_vals = accepted_df["Length(mm)"].values
    axes[1, 0].plot(length_vals, marker='o', color="black", label="Measured")

    # ✅ Nominal + tolerance reference lines
    axes[1, 0].axhline(nominal_length, color="blue", linestyle="-", label="Nominal")
    axes[1, 0].axhline(upper_tol_len, color="red", linestyle="--", label="Upper Tol")
    axes[1, 0].axhline(lower_tol_len, color="red", linestyle="--", label="Lower Tol")

    axes[1, 0].set_ylim(nominal_length - 6, nominal_length + 6)
else:
    axes[1, 0].text(0.5, 0.5, "No Accepted Screws", ha="center", va="center",
                    fontsize=14, color="red")

axes[1, 0].set_title("Length Trend (Accepted Screws)")
axes[1, 0].set_xlabel("Sample Index")
axes[1, 0].set_ylabel("Length (mm)")
axes[1, 0].grid(alpha=0.4, linestyle="--")
axes[1, 0].legend(loc="upper right")

# === Width Trend ===
if len(accepted_df) > 0:
    screw_type = accepted_df["Type"].iloc[0]
    nominal_width = SCREW_SPECS[screw_type]["width"]
    upper_tol_wid = nominal_width + TOLERANCE_MM
    lower_tol_wid = nominal_width - TOLERANCE_MM

    width_vals = accepted_df["Width(mm)"].values
    axes[1, 1].plot(width_vals, marker='o', color="black", label="Measured")

    axes[1, 1].axhline(nominal_width, color="blue", linestyle="-", label="Nominal")
    axes[1, 1].axhline(upper_tol_wid, color="red", linestyle="--", label="Upper Tol")
    axes[1, 1].axhline(lower_tol_wid, color="red", linestyle="--", label="Lower Tol")

    axes[1, 1].set_ylim(nominal_width - 6, nominal_width + 6)
else:
    axes[1, 1].text(0.5, 0.5, "No Accepted Screws", ha="center", va="center",
                    fontsize=14, color="red")

axes[1, 1].set_title("Width Trend (Accepted Screws)")
axes[1, 1].set_xlabel("Sample Index")
axes[1, 1].set_ylabel("Width (mm)")
axes[1, 1].grid(alpha=0.4, linestyle="--")
axes[1, 1].legend(loc="upper right")

plt.tight_layout(rect=[0, 0, 1, 0.95])
out_path = os.path.join(OUTPUT_FOLDER, "QC_Dashboard_Trend.png")
plt.savefig(out_path, dpi=150)
plt.close()

print("✅ Trend-based QC Dashboard saved at:", out_path)
