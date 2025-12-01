# 📘 Page Replacement Algorithm Simulator (GUI)

A modern, user-friendly FIFO Page Replacement Algorithm visualizer built using Python and CustomTkinter. 

This simulator demonstrates how the FIFO page replacement method works using a step-by-step animated visualization.

---

## Features
- **✔ Modern Dark UI** 
- **✔ Step-by-Step Animation**
- **✔ Clear Visualization**
    - Step number
    - Page accessed
    - Frame status after each step
    - Fault occurrence
    - Total page faults 
    - Hit ratio
- **✔ Input Controls**
    - Set reference string (up to 10 pages)
    - Choose number of frames (3, 4, or 5)
    - Reset all inputs easily

---

## 🚀 How to Run the Project
1. Install Python
```
Make sure Python 3.8+ is installed.
```

2. Install Dependencies
```
pip install customtkinter
```

3. Run the Simulator
```
python main.py
```

---

## 🔧 How It Works
- **FIFO (First-In-First-Out) Page Replacement**
    - The oldest loaded page is replaced first.
    - A queue is used to track the order of page arrival. 
    - For every page reference:
      - If the page is not in memory → Page Fault 
      - If frames are full → Replace the oldest page

---

## 📊 Output Example
```
========================= FIFO SIMULATION =========================
Reference String: [7, 0, 1, 2, 0, 3]
Number of Frames: 3

Step   Page     Frames After                  Fault
───────────────────────────────────────────────────────────────
1      7        7 - -                         YES
2      0        7 0 -                         YES
3      1        7 0 1                         YES
4      2        0 1 2                         YES
5      0        0 1 2                         No
6      3        1 2 3                         YES

==================================================================
TOTAL PAGE FAULTS: 5
HIT RATIO: 16.7%
==================================================================
```