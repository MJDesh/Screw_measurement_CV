# 🔩 Screw Measurement & Quality Inspection using OpenCV

A classical computer vision-based system that automatically measures and inspects industrial screws for dimensional accuracy using **Python**, **OpenCV**, and **Tkinter** — without any machine learning or deep learning.

---

## 🚀 Features

* Detects screws in images from a camera or smartphone
* Calculates **total length** and **width** in millimeters
* Quality control classification:

  * ✅ **ACCEPTED** if dimensions within tolerance
  * ❌ **REJECTED** otherwise
* Supports 3 screw types:

  * M6×25
  * M8×10
  * M8×16
* Full folder batch inspection
* Annotated results saved automatically
* CSV file generated with all measurements
* Lightweight UI for simple user interaction

---

## 📂 Project Structure

```
Screw_measurement_CV/
│
├── data_baba/             # Input screw images
├── results/               # Output annotated images & bounding boxes
├── screw_QC_UI.py         # Main script + Graphical User Interface
├── measurements.csv       # Generated results summary (after execution)
└── README.md              # Documentation (You are here)
```

---

## 🧠 How It Works

1️⃣ Load screw images from folder
2️⃣ Remove ruler region (fixed location → cropped out)
3️⃣ Convert to grayscale + apply Gaussian blur
4️⃣ Use Canny edge detection to extract screw shape
5️⃣ Find largest contour and compute rotated bounding box
6️⃣ Determine:

* Longest edge → **Screw Length**
* Shortest edge → **Width (diameter)**
  7️⃣ Convert pixels → millimeters using a calibrated scale
  8️⃣ Compare with expected screw size → QC decision
  9️⃣ Save processed result images + numeric measurements

---

## ✅ QC Logic (Accept / Reject)

```python
if abs(measured_value - expected_value) <= tolerance:
    status = "ACCEPTED"
else:
    status = "REJECTED"
```

---

## 🛠️ Installation

Install required dependencies:

```bash
pip install opencv-python numpy
```

> **Note:** Tkinter is included with most Python installations — no separate install needed.

---

## ▶️ How to Run

```bash
python screw_QC_UI.py
```

**Steps inside UI:**

1️⃣ Select folder path → e.g. `data_baba/`
2️⃣ Select screw type → `M6x25 / M8x10 / M8x16`
3️⃣ Click ✅ **Run Inspection**
4️⃣ Results are saved into:

```
results/            # annotated screw images
measurements.csv    # inspection summary report
```

---

## 📊 Sample Output (CSV)

| Image        | Length (mm) | Width (mm) | Status   |
| ------------ | ----------- | ---------- | -------- |
| screw_01.jpg | 25.01       | 6.05       | ACCEPTED |
| screw_05.jpg | 27.90       | 6.44       | REJECTED |

---

## 🔍 Computer Vision Techniques Used

| Technique                 | Purpose                  |
| ------------------------- | ------------------------ |
| Gaussian Blur             | Noise removal            |
| Canny Edge Detection      | Screw contour extraction |
| Largest Contour Selection | Screw detection          |
| Rotated Bounding Box      | Accurate geometry        |
| Pixels → mm Scaling       | Real-world measurement   |

---

## 🏭 Industrial Use Cases

* Automated assembly line QC
* Component measurement systems
* Smart manufacturing
* Engineering academic projects

---

## 🧱 Future Improvements

* Real-time measurement via webcam
* Automatic scale calibration using ruler detection
* Support for more fastener types
* Dashboard for analytics (rejection stats)

---

## 👨‍💻 Developers

**Name / Team Name**
**Department / Institution**
**Year:** 2025

---

## 📄 License

**MIT License** — free to use, modify, and distribute with attribution.
