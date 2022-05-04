#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys


def build_kustomize(pathname, dry_run_type=None):

    command = ["kustomize", "build", pathname]
    if dry_run_type:
        kustomize_cmd = ("kustomize", "build", pathname)
        kubectl_cmd = ("kubectl", f"--dry-run={dry_run_type}", "apply", "-f", "-")
        ps = subprocess.Popen(kustomize_cmd, stdout=subprocess.PIPE)
        result = subprocess.run(kubectl_cmd, stdin=ps.stdout)
        ps.wait()
    else:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    return result.returncode


def folder_kustomize(path):

    kustomize_files = ["kustomization.yaml", "kustomization.yml", "Kustomization"]
    files = os.listdir(path)

    if any(f in kustomize_files for f in files):
        return True

    return False


def main(argv=None):

    parser = argparse.ArgumentParser(
        description="Validates kustomization files and optionally runs kubectl --dry-run on result"
    )

    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )

    parser.add_argument(
        "-d",
        "--dry-run",
        nargs="?",
        type=str,
        help="Runs kubectl --dry-run across built kustomize with the specified mode.  Defualts to 'client'. Options 'client','server'",
    )

    args = parser.parse_args(argv)

    if not args.filenames:
        parser.print_help()
        return 1

    if args.dry_run:
        if args.dry_run.lower() not in ["client", "server"]:
            print(
                f"--dry-run passed, but type '{args.dry_run}' is not valid, must be 'client' or 'server'"
            )
            return 1

    # Strip filename from paths
    # as kustomize must be run against base dir
    paths = [os.path.dirname(f) for f in args.filenames]

    # remove any potential duplicates
    paths = list(set(paths))

    # Remove paths without kustomization file
    paths = [f for f in paths if folder_kustomize(f)]

    return_code = 0

    build_results = [f for f in paths if build_kustomize(f, args.dry_run)]

    for error_file in build_results:
        print(f"Kustomize build failed in file: {error_file}")
        return_code = True

    return return_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


def test_kustomize_pass():
    assert main(["./tests/kustomize-pass/"]) == 0


def test_kustomize_fail():
    assert main(["./tests/kustomize-fail/"]) == 1


def test_kustomize_dryrun_pass():
    assert main(["./tests/kustomize-pass/ --dry-run client"]) == 0


def test_kustomize_dryrun_fail():
    assert main(["./tests/kustomize-fail/ --dry-run client"]) == 1
