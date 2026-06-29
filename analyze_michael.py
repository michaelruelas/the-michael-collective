#!/usr/bin/env python3
import os
import re
from collections import defaultdict
from datetime import datetime

RESOURCES_DIR = "resources"
MICHAEL_VARIATIONS = {
    "Michael": ["Michael", "Micheal", "Mykel", "Michael"],
    "Miguel": ["Miguel"],
    "Michel": ["Michel"],
    "Michele": ["Michele"],
    "Mikhail": ["Mikhail", "Mikhail", "Mikhael"],
    "Michal": ["Michal"],
    "Mikael": ["Mikael", "Mikkel", "Mikaere"],
    "Micheal": ["Micheal"],
    "Michiel": ["Michiel"],
    "Mícheál": ["Mícheál", "Micheal"],
    "Mihangel": ["Mihangel"],
    "Mihály": ["Mihály"],
    "Mykhailo": ["Mykhailo"],
    "Mickey": ["Mickey", "Mick", "Mikey", "Mike", "Mitch", "Mich", "Misha"],
}

def normalize_name(name):
    return name.strip().lower()

def get_variant_set():
    variants = set()
    for canonical, vars in MICHAEL_VARIATIONS.items():
        variants.update(vars)
    return {v.lower() for v in variants}

MICHAEL_CANONICALS = get_variant_set()

def parse_year_file(filepath):
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 3:
                name, gender, count = parts[0], parts[1], int(parts[2])
                data.append((name, gender, count))
    return data

def extract_michael_data(data, year):
    results = []
    for name, gender, count in data:
        if normalize_name(name) in MICHAEL_CANONICALS:
            canonical = None
            for canon, vars in MICHAEL_VARIATIONS.items():
                if normalize_name(name) in [v.lower() for v in vars]:
                    canonical = canon
                    break
            results.append({
                "year": year,
                "name": name,
                "canonical": canonical or name,
                "gender": gender,
                "count": count
            })
    return results

def get_all_years():
    files = [f for f in os.listdir(RESOURCES_DIR) if f.startswith('yob') and f.endswith('.txt')]
    years = []
    for f in files:
        match = re.search(r'yob(\d{4})\.txt', f)
        if match:
            years.append(int(match.group(1)))
    return sorted(years)

def analyze():
    years = get_all_years()
    all_michael_data = []
    yearly_totals = defaultdict(int)
    yearly_by_gender = defaultdict(lambda: {"M": 0, "F": 0})
    yearly_by_variant = defaultdict(lambda: defaultdict(int))
    all_names_by_year = defaultdict(dict)

    for year in years:
        filepath = os.path.join(RESOURCES_DIR, f"yob{year}.txt")
        if not os.path.exists(filepath):
            continue
        data = parse_year_file(filepath)

        michael_data = extract_michael_data(data, year)
        all_michael_data.extend(michael_data)

        name_counts = {}
        for entry in michael_data:
            key = entry["canonical"]
            name_counts[key] = name_counts.get(key, 0) + entry["count"]
            yearly_totals[year] += entry["count"]
            yearly_by_gender[year][entry["gender"]] += entry["count"]
            yearly_by_variant[year][entry["canonical"]] += entry["count"]

        all_names_by_year[year] = name_counts

    return {
        "years": years,
        "all_data": all_michael_data,
        "yearly_totals": dict(yearly_totals),
        "yearly_by_gender": dict(yearly_by_gender),
        "yearly_by_variant": dict(yearly_by_variant),
        "all_names_by_year": dict(all_names_by_year)
    }

def format_number(n):
    if n >= 1000000:
        return f"{n/1000000:.1f}M"
    elif n >= 1000:
        return f"{n/1000:.1f}K"
    return str(n)

if __name__ == "__main__":
    results = analyze()

    print("=" * 60)
    print("🇺🇸 THE MICHAEL COLLECTIVE - FULL DRILL DOWN")
    print("=" * 60)

    print(f"\n📊 DATASET: US Census Baby Names {min(results['years'])}-{max(results['years'])}")
    print(f"   Total years analyzed: {len(results['years'])}")

    print("\n" + "=" * 60)
    print("🔥 THE PEAK ERA: When MichaelDOMINATED")
    print("=" * 60)

    sorted_years = sorted(results['yearly_totals'].items(), key=lambda x: x[1], reverse=True)
    print("\nTop 10 Michael Years (by total count):")
    for i, (year, count) in enumerate(sorted_years[:10], 1):
        print(f"  {i}. {year}: {format_number(count):>8} Michaels born")

    peak_year = sorted_years[0][0]
    peak_count = sorted_years[0][1]

    print(f"\n🏆 PEAK YEAR: {peak_year}")
    print(f"   {format_number(peak_count)} babies named Michael that year")

    if peak_year in results['yearly_by_gender']:
        genders = results['yearly_by_gender'][peak_year]
        total_m = genders.get('M', 0)
        total_f = genders.get('F', 0)
        print(f"   Male: {format_number(total_m):>8} ({total_m/peak_count*100:.1f}%)")
        print(f"   Female: {format_number(total_f):>8} ({total_f/peak_count*100:.1f}%)")

    print("\n" + "=" * 60)
    print("📈 THE RISE AND FALL: Michael Over Time")
    print("=" * 60)

    decades = {}
    for year, count in results['yearly_totals'].items():
        decade = (year // 10) * 10
        decades[decade] = decades.get(decade, 0) + count

    print("\nMichael births by decade:")
    for decade in sorted(decades.keys()):
        bar = "█" * int(decades[decade] / 50000)
        print(f"  {decade}s: {bar} {format_number(decades[decade])}")

    print("\n" + "=" * 60)
    print("🌍 GLOBAL variations: Miguel, Michel, Mikhail & more")
    print("=" * 60)

    variant_totals = defaultdict(int)
    for year, variants in results['yearly_by_variant'].items():
        for variant, count in variants.items():
            variant_totals[variant] += count

    sorted_variants = sorted(variant_totals.items(), key=lambda x: x[1], reverse=True)
    print("\nAll Michael variations (total births, all time):")
    for variant, total in sorted_variants:
        bar = "█" * int(total / 100000)
        print(f"  {variant:>12}: {bar} {format_number(total)}")

    print("\n" + "=" * 60)
    print("⚥ GENDER BREAKDOWN: The Michael spectrum")
    print("=" * 60)

    male_total = sum(g.get('M', 0) for g in results['yearly_by_gender'].values())
    female_total = sum(g.get('F', 0) for g in results['yearly_by_gender'].values())
    total_all = male_total + female_total

    print(f"\n  👨 Male Michaels:  {format_number(male_total):>10} ({male_total/total_all*100:.2f}%)")
    print(f"  👩 Female Michaels: {format_number(female_total):>9} ({female_total/total_all*100:.2f}%)")
    print(f"  📊 Total tracked:   {format_number(total_all):>10}")

    print("\n" + "=" * 60)
    print("📉 THE DECLINE: When did Michael stop being #1?")
    print("=" * 60)

    if 2000 in results['yearly_totals']:
        y2000 = results['yearly_totals'][2000]
        y2024 = results['yearly_totals'].get(2024, results['yearly_totals'].get(2023, 0))
        decline = ((y2000 - y2024) / y2000) * 100
        print(f"\n  2000: {format_number(y2000):>8} Michaels")
        print(f"  2024: {format_number(y2024):>8} Michaels")
        print(f"  📉 Decline: {decline:.1f}%")

    recent_years = [y for y in sorted(results['yearly_totals'].keys()) if y >= 2015]
    print("\nRecent years (post-peak):")
    for year in recent_years:
        count = results['yearly_totals'][year]
        bar = "█" * int(count / 500)
        print(f"  {year}: {bar} {format_number(count)}")

    print("\n" + "=" * 60)
    print("🏅 FUN FACTS & SLACK BULLETINS")
    print("=" * 60)

    peak_decade = max(decades, key=decades.get)
    print(f"""
🎯 FOR #the-michael-collective:

• Michael was #1 boys name for 44 consecutive years (1954-1997)
• Peak year {peak_year} saw {format_number(peak_count)} Michaels born
• That's roughly {peak_count/(365.25*24):.0f} Michaels born EVERY HOUR in {peak_year}
• Total Michaels born since {min(results['years'])}: {format_number(total_all):>10}
• Michael still #3 in 2024 with {format_number(results['yearly_totals'].get(2024, 0))} babies

🌍 Global variations tracked:
  • Miguel (Spanish/Portuguese) - still going strong
  • Michel (French) - classic European
  • Mikhail/Misha (Russian) - Eastern European heritage
  • Mick/Mikey/Mike (nicknames) - American classics

⚡ The Michael Collective spans {len(results['years'])} years of census data
   and includes {len(sorted_variants)} distinct name variations.
""")

    print("=" * 60)
    print("RAW DATA: Year-by-year totals")
    print("=" * 60)
    for year in sorted(results['yearly_totals'].keys()):
        print(f"  {year}: {results['yearly_totals'][year]:>8}")