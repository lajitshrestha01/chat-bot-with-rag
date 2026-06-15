#!/usr/bin/env python3
import sys
from cli.main import main

# Override default folder if no --folder provided
sys.argv = [a for a in sys.argv if not a.startswith("--folder")]
if len(sys.argv) > 1 and sys.argv[1] == "ingest" and "--folder" not in sys.argv:
    sys.argv.insert(2, "--folder")
    sys.argv.insert(3, "data/raw_pdfs")

if __name__ == "__main__":
    main()