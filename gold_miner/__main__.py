"""Command line scanner: python -m gold_miner records.csv"""
import argparse
import json
from .scanner import scan_csv

def main():
    parser = argparse.ArgumentParser(description="Review public-record surplus CSV exports")
    parser.add_argument("csv_file", help="CSV with public case records")
    parser.add_argument("--output", help="Optional JSON output file")
    args = parser.parse_args()
    output = json.dumps(scan_csv(args.csv_file), indent=2)
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()
