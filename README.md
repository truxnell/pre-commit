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

## Pre-release

* **kustomize-build** - Ensure modified kustomize files render

## Planned

* **helm-release-lint** - Lint a helm release file with values in file
* **kubeval-dryrun** - Apply each yaml manifest with `kubeval --dry-run=server` to ensure file will apply to server
* **kubeconform-lint** - Lint each yaml with kubeconform
