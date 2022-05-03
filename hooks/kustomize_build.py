#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from typing import Sequence


def build_kustomize(pathname):

    result = subprocess.run(
        ["kustomize", "build", pathname],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode


def main(argv=None):

    parser = argparse.ArgumentParser(description="Validates kustomization files")
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )
    args = parser.parse_args(argv)

    if not args.filenames:
        print("No arguments passed to kustomize_build")

    # Strip filename from paths
    # as kustomize must be run against base dir
    paths = [os.path.dirname(f) for f in args.filenames]

    # remove any potential duplicates
    paths = list(set(paths))

    return_code = 0

    build_results = [f for f in paths if build_kustomize(f)]

    for error_file in build_results:
        print(f"Kustomize build failed in file: {error_file}")
        return_code = 1

    return return_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


def test_kustomize_pass():
    assert main(["./tests/kustomize-pass/"]) == 0


def test_kustomize_fail():
    assert main(["./tests/kustomize-fail/"]) == 1
