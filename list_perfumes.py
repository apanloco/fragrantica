#!/usr/bin/env python3
"""List perfumes sorted by rating, filtered by minimum number of ratings."""

import argparse
import csv
import os
import sys


def load_perfumes(path):
    perfumes = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rating = float(row["Rating Value"])
                # Rating Count may contain commas as thousands separators
                count = int(row["Rating Count"].replace(",", ""))
            except (ValueError, KeyError):
                continue
            name = row["Name"].strip()
            gender = row.get("Gender", "").strip()
            # The CSV has the gender glued onto the name (e.g. "Anais Anais Cacharelfor women")
            if gender and name.endswith(gender):
                name = name[: -len(gender)].strip()
            perfumes.append(
                {
                    "name": name,
                    "gender": gender,
                    "rating": rating,
                    "count": count,
                    "url": row.get("url", "").strip(),
                }
            )
    return perfumes


def main():
    parser = argparse.ArgumentParser(
        description="List Fragrantica perfumes sorted by rating."
    )
    parser.add_argument(
        "--min-ratings",
        type=int,
        default=200,
        help="Minimum number of ratings/comments (default: 200)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="Show only the top N results",
    )
    parser.add_argument(
        "--asc",
        action="store_true",
        help="Sort ascending instead of descending",
    )
    parser.add_argument(
        "--gender",
        type=str,
        default=None,
        choices=["women", "men", "both"],
        help="Filter by gender: 'women', 'men', or 'both' (unisex)",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Path to the CSV file (default: data/fra_perfumes.csv next to this script)",
    )
    args = parser.parse_args()

    if args.csv:
        csv_path = args.csv
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, "data", "fra_perfumes.csv")

    if not os.path.isfile(csv_path):
        print(f"Error: CSV file not found at {csv_path}", file=sys.stderr)
        print("", file=sys.stderr)
        print("To get the data, run:  bash setup.sh", file=sys.stderr)
        print(
            "Or download it from: https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset",
            file=sys.stderr,
        )
        print("See README.md for details.", file=sys.stderr)
        sys.exit(1)

    perfumes = load_perfumes(csv_path)
    filtered = [p for p in perfumes if p["count"] >= args.min_ratings]
    filtered.sort(key=lambda p: p["rating"], reverse=not args.asc)

    if args.gender:
        gender_map = {
            "women": "for women",
            "men": "for men",
            "both": "for women and men",
        }
        target = gender_map[args.gender]
        filtered = [p for p in filtered if p["gender"].lower() == target]

    if args.top:
        filtered = filtered[: args.top]

    print(f"{'#':<6} {'Rating':<8} {'Count':<8} {'Name'}")
    print("-" * 80)
    for i, p in enumerate(filtered, 1):
        url = p["url"]
        # OSC 8 hyperlink escape sequence (clickable in modern terminals)
        label = f"{p['name']} ({p['gender']})" if p["gender"] else p["name"]
        link = f"\033]8;;{url}\033\\{label}\033]8;;\033\\" if url else label
        print(f"{i:<6} {p['rating']:<8.2f} {p['count']:<8} {link}")

    print(f"\nTotal: {len(filtered)} perfumes (min {args.min_ratings} ratings)")


if __name__ == "__main__":
    main()
