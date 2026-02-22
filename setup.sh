#!/usr/bin/env bash
# Download and extract the Fragrantica perfume dataset.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
CSV="$DATA_DIR/fra_perfumes.csv"
DATASET="olgagmiufana1/fragrantica-com-fragrance-dataset"
# kaggle names the zip after the dataset slug
KAGGLE_ZIP="$SCRIPT_DIR/fragrantica-com-fragrance-dataset.zip"

if [ -f "$CSV" ]; then
    echo "Data already exists at $CSV — skipping download."
    exit 0
fi

mkdir -p "$DATA_DIR"

# Find an existing zip, or download one
ARCHIVE=""
for f in "$KAGGLE_ZIP" "$SCRIPT_DIR/archive.zip"; do
    if [ -f "$f" ]; then
        ARCHIVE="$f"
        break
    fi
done

if [ -z "$ARCHIVE" ]; then
    if command -v kaggle &>/dev/null; then
        echo "Downloading dataset via kaggle CLI…"
        kaggle datasets download -d "$DATASET" -p "$SCRIPT_DIR"
        ARCHIVE="$KAGGLE_ZIP"
    else
        echo "kaggle CLI not found."
        echo ""
        echo "Option 1: Install it and re-run this script:"
        echo "  pip install kaggle"
        echo ""
        echo "Option 2: Download manually from:"
        echo "  https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset"
        echo ""
        echo "Then extract into data/:"
        echo "  unzip archive.zip -d data"
        exit 1
    fi
fi

echo "Extracting $ARCHIVE…"
unzip -o "$ARCHIVE" -d "$DATA_DIR"
echo "Done. Data is at $CSV"
