# HIT137 – Assignment 2

This repository contains the required code and files for **Assignment 2**.  
It includes solutions for all three questions, along with input and output files.

---

## Quick start
- Make sure Python 3.8+ is installed.  
- For Question 2, `pandas` and `numpy` are required:  
  ```bash
  pip install pandas numpy
  ```
- Each question has its own script. Run them from the repository root as shown below.

---

## Repository structure
```
Assignment-2/
│
├── encrypt.py                        # Question 1 main script
├── temperature.py                    # Question 2 main script
├── pattern.py                        # Question 3 turtle graphics
│
├── raw_text.txt                      # Input file for Q1
├── encrypted_text.txt                # Generated output (Q1)
├── decrypted_text.txt                # Generated output (Q1)
│
├── temperatures/                     # Folder with CSVs for Q2
│   └── (multiple .csv files, one per year)
│
├── average_temp.txt                  # Q2 output
├── largest_temp_range_station.txt    # Q2 output
├── temperature_stability_stations.txt# Q2 output
│
└── README.md
```

---

## Question 1 – Text Encryption / Decryption

**Description**  
Reads `raw_text.txt`, encrypts its contents using two user-provided shift values, writes `encrypted_text.txt`, then attempts to decrypt and verify the result against the original.

**Run**
```bash
python encrypt.py
```

**Behaviour**
1. Prompts for two integers (`shift1`, `shift2`).
2. Applies the encryption rules for lowercase and uppercase letters according to the assignment specification.
3. Writes encrypted text to `encrypted_text.txt`.
4. Decrypts using the implemented method and writes `decrypted_text.txt`.
5. Prints whether the decrypted text matches `raw_text.txt`.

**Notes / important details**
- The assignment rules can produce collisions (different original letters mapping to the same encrypted character) for some shift values. In those cases the program will correctly report `FAIL` during verification. This is expected behaviour given the rules.
---

## Question 2 – Temperature Data Analysis

**Description**  
Process all CSV files in the `temperatures/` folder (each file typically represents one year) and compute:
- seasonal averages (Australian seasons),
- station(s) with the largest temperature range,
- station(s) with smallest and largest standard deviation (most stable / most variable).

**Run**
```bash
python temperature.py
```

**Output files**
- `average_temp.txt` — seasonal averages (Summer, Autumn, Winter, Spring).  
- `largest_temp_range_station.txt` — station(s) with the largest recorded range and their max/min values.  
- `temperature_stability_stations.txt` — most stable and most variable station(s) with stddev values.

**Accepted input formats**
- **Long format**: columns like `Date`, `Station`, `Temperature` (or `Temp`).  
- **Wide format**: first column is a date and remaining columns are station names with temperature values.  
- The script attempts to be robust and also supports a common station-as-rows layout (first column station id, remaining columns month names).

**Assumptions**
- Missing values (NaN) are ignored in calculations.
- Seasons are defined as:
  - Summer: December–February
  - Autumn: March–May
  - Winter: June–August
  - Spring: September–November

**If outputs look wrong**
- Inspect the CSV headers: unusual layouts can cause misinterpretation (e.g., months as headers, stations as rows). If needed, open one CSV and paste the first few lines into an issue or update the CSV to a supported layout.

---

## Question 3 – Recursive Polygon Pattern

**Description**  
Use `turtle` to draw a regular polygon where each edge is recursively modified: divide an edge into 3 parts and replace the middle third with two sides of an equilateral triangle pointing inward (an inward "indentation"). Repeat to the requested recursion depth.

**Run**
```bash
python pattern.py
```

**Inputs**
- Number of sides (integer ≥ 3)  
- Side length (pixels, float > 0)  
- Recursion depth (integer ≥ 0)  

**Behaviour**
- Depth 0 draws a regular polygon.  
- Each depth increases complexity: each straight segment is replaced by 4 segments (growth ≈ n × 4^depth).  
- The script adjusts the drawing viewport so the figure is not clipped on typical screens.

**Performance notes**
- The number of segments grows quickly. For large `depth` and/or many sides this may be slow. The script warns before drawing very large fractals.

**Suggested example**
- `sides = 4`, `side_length = 300`, `depth = 3` — a good example that demonstrates the recursion without being excessively slow.

---

## General notes

- Tested with Python 3.8+.  
- Only standard libraries are used for Q1 and Q3. Question 2 requires `pandas` and `numpy`.  
- Output files are plain text for easy inspection.  
- If a script raises an error, check that required input files are present (`raw_text.txt` for Q1, CSVs in `temperatures/` for Q2) and that inputs are valid.

---

## Troubleshooting / tips

- If Q1 verification returns `FAIL`, try different (small) shifts or use the metadata-enabled version.  
- If Q2 outputs seem off, open one CSV in a text editor and confirm the layout/headers match one of the accepted formats.  
- If Q3 is clipped or partially off-screen, reduce the side length or recursion depth, or run the script and allow it to set the window size (it adjusts world coordinates automatically).

---

