# Fragrantica Perfume Rankings

Browse and filter perfumes from the [Fragrantica](https://www.fragrantica.com/) dataset, sorted by rating. Perfume names are clickable links to their Fragrantica page (in supported terminals).

## Requirements

- Python 3.6+

## Getting the data

The quickest way is to run the setup script:

```bash
bash setup.sh
```

This will use the `kaggle` CLI to download the dataset automatically. If you don't have it installed, the script prints a manual download link.

**Manual setup:**

1. Download the [Fragrantica.com Fragrance Dataset](https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset) from Kaggle.
2. Extract `archive.zip` into a `data/` directory:

```bash
unzip archive.zip -d data
```

You should end up with `data/fra_perfumes.csv`.

> **Note:** The archive also contains `fra_cleaned.csv`, a pre-cleaned version of the dataset. This script uses `fra_perfumes.csv` (the full, original data).

## Usage

```bash
python list_perfumes.py
```

By default this lists all perfumes with **200+ ratings**, sorted by rating (highest first).

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--min-ratings N` | Minimum number of ratings | 200 |
| `--top N` | Show only the top N results | all |
| `--asc` | Sort ascending (lowest first) | descending |
| `--gender GENDER` | Filter by gender: `women`, `men`, or `both` (unisex) | all |
| `--csv PATH` | Path to the CSV file | `data/fra_perfumes.csv` next to the script |

### Examples

```bash
python list_perfumes.py --top 50                        # top 50 perfumes
python list_perfumes.py --min-ratings 1000              # only perfumes with 1000+ ratings
python list_perfumes.py --gender women --top 20   # top 20 women's perfumes
python list_perfumes.py --gender men --asc         # worst-rated men's perfumes
python list_perfumes.py --csv ~/my_data/fra_perfumes.csv  # use a custom CSV path
```

### Sample output

```
#      Rating   Count    Name
--------------------------------------------------------------------------------
1      4.71     244      Hard Candy Elixir Aaron Terence Hughes
2      4.70     338      Vol de Nuit Extract Guerlain
3      4.68     982      Valentino Uomo Intense 2021 Valentino
...

Total: 1245 perfumes (min 200 ratings)
```

> **Tip:** Perfume names are rendered as clickable hyperlinks using [OSC 8](https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda) escape sequences. This works in most modern terminals (iTerm2, GNOME Terminal, Windows Terminal, WezTerm, etc.). In terminals that don't support it, names appear as plain text.
