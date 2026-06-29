#!/usr/bin/env python3
import os
import re
import json
from collections import defaultdict

RESOURCES_DIR = "resources"

def parse_year_file(filepath):
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 3:
                name, gender, count = parts[0], parts[1], int(parts[2])
                data.append((name, gender, count))
    return data

def get_rank(data, target_name, target_gender):
    sorted_data = sorted(data, key=lambda x: x[2], reverse=True)
    rank = 1
    for name, gender, count in sorted_data:
        if name.lower() == target_name.lower() and gender == target_gender:
            return rank
        rank += 1
    return None

def get_michael_data_for_year(filepath):
    michael_entries = []
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 3:
                name, gender, count = parts[0], parts[1], int(parts[2])
                if name.lower() == 'michael':
                    michael_entries.append({'name': name, 'gender': gender, 'count': count})
    return michael_entries

def analyze_rankings():
    files = [f for f in os.listdir(RESOURCES_DIR) if f.startswith('yob') and f.endswith('.txt')]
    years_data = []

    for f in sorted(files):
        match = re.search(r'yob(\d{4})\.txt', f)
        if not match:
            continue
        year = int(match.group(1))
        filepath = os.path.join(RESOURCES_DIR, f)

        data = parse_year_file(filepath)
        michael_entries = get_michael_data_for_year(filepath)

        for entry in michael_entries:
            rank = get_rank(data, entry['name'], entry['gender'])
            entry['year'] = year
            entry['rank'] = rank

        male_michael = next((e for e in michael_entries if e['gender'] == 'M'), None)

        years_data.append({
            'year': year,
            'total_michaels': sum(e['count'] for e in michael_entries),
            'male_count': male_michael['count'] if male_michael else 0,
            'male_rank': male_michael['rank'] if male_michael else None,
            'female_count': next((e['count'] for e in michael_entries if e['gender'] == 'F'), 0)
        })

    return years_data

if __name__ == "__main__":
    rankings = analyze_rankings()

    print("=" * 60)
    print("📊 MICHAEL'S RANK OVER TIME (Male)")
    print("=" * 60)

    print("\nYear | Rank  | Michaels | Trend")
    print("-" * 50)

    prev_rank = None
    for r in rankings:
        if r['male_rank'] is None:
            continue
        arrow = ""
        if prev_rank is not None:
            diff = prev_rank - r['male_rank']
            if diff > 0:
                arrow = " 📈"
            elif diff < 0:
                arrow = " 📉"
            else:
                arrow = " ➡️"
        print(f" {r['year']} | #{r['male_rank']:>5} | {r['male_count']:>7,} |{arrow}")
        prev_rank = r['male_rank']

    peak_rank = min(r for r in rankings if r['male_rank'] is not None)
    print(f"\n🏆 Best rank: #{peak_rank['male_rank']} in {peak_rank['year']} with {peak_rank['male_count']:,} babies")

    with open('michael_slack_data.json', 'w') as f:
        json.dump({
            'analysis_date': str(__import__('datetime').date.today()),
            'source': 'US Census Baby Names 1880-2025',
            'rankings': rankings
        }, f, indent=2)

    print("\n✅ Saved to michael_slack_data.json")