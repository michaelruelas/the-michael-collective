# The Michael Collective — Agent Instructions

## Purpose
This repo analyzes US Census baby name data to explore Michael's 146-year dominance, global variations, and naming trends.

## Data
- **Location:** `resources/yob*.txt`
- **Format:** CSV with columns `name,gender,count`
- **Range:** 1880-2025 (146 years, 100+ files, 10M+ records)
- **Variations tracked:** Michael, Mickey, Miguel, Michel, Michele, Michal, Mikhail, Mikael (and nicknames Mike, Mick, Misha, etc.)

## Scripts

### slack_report.py (Primary)
```bash
python3 slack_report.py
```
Generates full Slack Canvas report with tables, ASCII charts, emoji. Copy-paste ready for #the-michael-collective.

### analyze_michael.py
```bash
python3 analyze_michael.py
```
Core analysis: decade trends, peaks, gender splits, variation totals.

### analyze_rank.py
```bash
python3 analyze_rank.py
```
Year-by-year ranking trajectory from #115 (1880) to #27 (2024).

## Key Stats (as of June 2026)

| Metric | Value |
|--------|-------|
| Peak Year | 1958 |
| Peak Count | 113,854 |
| #1 Duration | 44 years (1954-1997) |
| Total Michaels | 5.3M+ |
| Current Rank | #27 (2024) |

## Adding New Data
1. Download new `yobYYYY.txt` from US Census
2. Place in `resources/` directory
3. Re-run `python3 slack_report.py` — updates automatically

## Output Files
Generated files (`.json`, `.csv`, `__pycache__/`) are gitignored.

## Slack Integration
Use `slack_canvas_content.md` as-is for Slack Canvas. Tables and emoji render natively.