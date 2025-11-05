import cv2
import numpy as np
import os
import csv
import glob
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ---------------- SCREW TYPE DATABASE ----------------
SCREW_SPECS = {
    "M6x25": {"length": 31.0, "width": 10.0},
    "M8x10": {"length": 18.0, "width": 13.0},
    "M8x16": {"length": 24.0, "width": 13.0},
}

TOLERANCE_MM = 1.5
PIXELS_PER_MM = 10.0
RULER_TOP = 860

OUTPUT_FOLDER = "results"
CSV_FILE = "results/measurements.csv"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ---------------- MEASUREMENT FUNCTION ----------------
def measure_screw(image, screw_type):
    screw_region = image[:RULER_TOP, :]

    gray = cv2.cvtColor(screw_region, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7,7), 0)

    edges = cv2.Canny(gray, 50, 150)
    edges = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=1)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None

    c = max(contours, key=cv2.contourArea)

    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect).astype(int)

    (w_px, h_px) = rect[1]

    length_px = max(w_px, h_px)
    width_px = min(w_px, h_px)

    length_mm = length_px / PIXELS_PER_MM
    width_mm = width_px  / PIXELS_PER_MM

    expected_len = SCREW_SPECS[screw_type]["length"]
    expected_wid = SCREW_SPECS[screw_type]["width"]

    ok_len = abs(length_mm - expected_len) <= TOLERANCE_MM
    ok_wid = abs(width_mm  - expected_wid) <= TOLERANCE_MM
    status = "ACCEPTED" if (ok_len and ok_wid) else "REJECTED"

    return length_mm, width_mm, status, box


# ---------------- PROCESS FOLDER ----------------
def process_folder(folder, screw_type):
    if not folder:
        messagebox.showwarning("Warning", "Please select a folder")
        return

    images = glob.glob(os.path.join(folder, "*.jpg"))
    if len(images) == 0:
        messagebox.showerror("Error", "No .jpg images in folder!")
        return

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Image","Length(mm)","Width(mm)","Status","Type"])

    for img_path in images:
        img_name = os.path.basename(img_path)
        img = cv2.imread(img_path)

        result = measure_screw(img, screw_type)
        if result is None:
            print(f"{img_name}: No screw detected")
            continue

        length_mm, width_mm, status, box = result

        output = img.copy()
        color = (0,180,0) if status=="ACCEPTED" else (0,0,255)

        cv2.drawContours(output, [box], -1, color, 3)
        cv2.putText(output, f"L:{length_mm:.2f}mm W:{width_mm:.2f}mm",
                    (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
        cv2.putText(output, status, (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        cv2.putText(output, screw_type, (30, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

        cv2.imwrite(os.path.join(OUTPUT_FOLDER, img_name), output)

        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([img_name,
                             f"{length_mm:.2f}",
                             f"{width_mm:.2f}",
                             status,
                             screw_type])

        print(f"{img_name}: {length_mm:.2f}mm, {width_mm:.2f}mm → {status}")

    messagebox.showinfo("✅ Done", "Inspection completed!")


# ---------------- GUI ----------------
def browse_folder():
    folder = filedialog.askdirectory()
    folder_var.set(folder)


root = tk.Tk()
root.title("Screw QC Inspection System")
root.geometry("500x350")

folder_var = tk.StringVar()
screw_type_var = tk.StringVar(value="M6x25")

tk.Label(root, text="Select image folder:", font=("Arial", 11)).pack(pady=10)
tk.Entry(root, textvariable=folder_var, width=45).pack(pady=5)
tk.Button(root, text="Browse", command=browse_folder,
          width=12, bg="lightblue").pack(pady=5)

tk.Label(root, text="Choose Screw Type:", font=("Arial", 11)).pack(pady=10)
ttk.Combobox(root, textvariable=screw_type_var,
             values=list(SCREW_SPECS.keys()),
             state="readonly", width=15).pack(pady=5)

tk.Button(root, text="Run Inspection ✅",
          command=lambda: process_folder(folder_var.get(), screw_type_var.get()),
          width=22, bg="lightgreen", font=("Arial", 12)).pack(pady=20)

tk.Button(root, text="Quit", command=root.destroy,
          width=12, bg="red", fg="white").pack(pady=10)

root.mainloop()
