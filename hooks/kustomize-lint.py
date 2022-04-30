#!/usr/bin/env python3
import argparse
import subprocess
from typing import Sequence


def build_kustomize(filename):

    result = subprocess.run(
        ["kustomize", "build", "tests/kustomize-fail/"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode


def main(argv: Sequence[str] | None = None) -> int:

    parser = argparse.ArgumentParser(description="Validates kustomization files")
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )
    parser.add_argument(
        "--enforce-all",
        action="store_true",
        help="Enforce all files are checked, not just staged files.",
    )
    args = parser.parse_args(argv)

    return_code = 0

    build_results = [f for f in args.filename if build_kustomize(f)]

    for error_file in build_results:
        print("Kustomize build failed in file: {0}".format(error_file))
        return_code = 1

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
