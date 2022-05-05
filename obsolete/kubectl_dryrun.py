#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

import yaml
from yaml.loader import SafeLoader


def is_k8s_manifest(filename):

    file = open(filename)
    data = yaml.load_all(file, Loader=SafeLoader)

    try:
        for f in data:

            # Check if valid k8s manifest
            if f.get("apiVersion", False) and f.get("kind", False):

                # Manifest is valid
                # Check if a SOPS key is present
                if f.get("sops", False):

                    # Skip file - we cant check SOPS files
                    return False
                return True
    except:
        return False

    return False


def kubectl_dryrun(filename, dry_run_type):

    result = subprocess.run(
        ["kubectl", "apply", f"--dry-run={dry_run_type}", "-f", filename],
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
    parser.add_argument(
        "-s",
        "--server",
        dest="type",
        action="store_const",
        const="server",
        default="client",
        help="dry-run type",
    )
    args = parser.parse_args(argv)

    if not args.filenames:
        return False

    # remove any potential duplicates
    paths = list(set(args.filenames))
    type = args.type
    return_code = 0

    paths = [
        f
        for f in paths
        if os.path.split(f)[1]
        not in ("kustomization.yaml", "kustomization.yml", "kustomization.yml")
    ]

    paths = [f for f in paths if is_k8s_manifest(f)]

    if not paths:
        print("No valid files passed for validation (Kustomizations are not validated)")
        return False

    build_results = [f for f in paths if kubectl_dryrun(f, type)]

    for error_file in build_results:
        print(f"Kubeval ({type} dry-run) apply failed in file: {error_file}")
        return_code = True

    return return_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


def test_kustomize_pass():
    files = [
        "tests/kustomize-pass/deployment.yaml",
        "tests/kustomize-pass/service.yaml",
    ]
    assert main(files) == 0


def test_kustomize_fail():
    files = [
        "tests/kustomize-fail/deployment.yaml",
        "tests/kustomize-fail/service.yaml",
    ]
    assert main(files) == 1
