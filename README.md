# 🇺🇸 The Michael Collective

**146 years of American naming history — analyzed, visualized, and ready for #the-michael-collective**

Analyze US Census baby name data to explore Michael's dominance, global variations, and naming trends from 1880-2025.

## Quick Start

```bash
# Generate Slack report
python3 slack_report.py

# Run core analysis
python3 analyze_michael.py

# Check ranking trajectory
python3 analyze_rank.py
```

## What's Inside

```
the-michael-collective/
├── resources/          # US Census baby name files (yob1880.txt - yob2025.txt)
├── analyze_michael.py  # Core analysis: trends, peaks, variations
├── analyze_rank.py     # Ranking trajectory over time
├── slack_report.py     # Slack Canvas-ready formatted report
└── slack_canvas_content.md  # Copy-paste content for #the-michael-collective
```

## Key Findings

| Metric | Value |
|--------|-------|
| Peak Year | 1958 (113,854 Michaels) |
| #1 Rank Duration | 44 years (1954-1997) |
| Total Michaels | 5.3M+ since 1880 |
| 2024 Rank | #27 |
| Decline from Peak | 90.1% |

## Tracked Variations

| Variation | Heritage | Total |
|-----------|----------|-------|
| Michael | 🇺🇸 English | 4.6M |
| Mickey | 🇺🇸 Nickname | 255K |
| Michele | 🇮🇹 Italian | 226K |
| Miguel | 🇪🇸 Spanish | 192K |
| Michel | 🇫🇷 French | 14K |
| Mikhail | 🇷🇺 Russian | 5K |
| Mikael | 🇸🇪 Nordic | 7K |

## For #the-michael-collective

Copy `slack_canvas_content.md` directly into a Slack Canvas page — formatting renders natively in Slack.

## Data Source

US Census Bureau Baby Names Dataset — 146 years, 100+ files, 10M+ records.

## Scripts

### slack_report.py
Generates a full Slack-ready report with ASCII charts, tables, and emoji. Run anytime to refresh stats.

### analyze_michael.py
Core data extraction and analysis — decade breakdowns, variation tracking, gender splits.

### analyze_rank.py
Tracks Michael's ranking position year-by-year from #115 (1880) to #27 (2024).