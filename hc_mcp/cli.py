#!/usr/bin/env python3
import argparse
from pathlib import Path
from hc_mcp.indexer import index_docs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--src", action="append", required=True)
    args = parser.parse_args()

    srcs = [Path(s) for s in args.src]
    db_path = Path(args.db)
    indexed, skipped = index_docs(srcs, db_path)
    print(f"Indexed {indexed} files, skipped {skipped}. DB: {db_path}")


if __name__ == "__main__":
    main()
