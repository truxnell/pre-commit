# Pre-commit hooks

This is a WIP repository for a few planned pre-commit hooks.  These are aimed to make life easier with using k8s in a gitops fashion.

## Installing

To install, add the following to a file in the root of your repository `.pre-commit-config.yaml`, and run `pre-commit install`

```yaml
  - repo: https://github.com/Truxnell/pre-commit
    rev: v0.0.1
    hooks:
      - id: kustomize_build
```

This hook will then run each push:

## Manual run / Run on entire repo

Pre-commit only checks changed files in the current commit.  It can be beneficial to run on all files at times:

You can run

```bash
pre-commit run -a          # or --all-files
```

To run pre-commit on your entire repo with a single hook

```bash
pre-commit kustomize_build -a
```

Alternatively, to run a single

## Pre-release

* **kustomize-build** - Ensure modified kustomize files render

## Planned

* **helm-release-lint** - Lint a helm release file with values in file
* **kubeval-dryrun** - Apply each yaml manifest with `kubeval --dry-run=server` to ensure file will apply to server
* **kubeconform-lint** - Lint each yaml with kubeconform
