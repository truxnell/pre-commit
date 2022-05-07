# Pre-commit hooks

This is a WIP repository for a few planned pre-commit hooks.  These are aimed to make life easier with using k8s in a gitops fashion.

## Installing

To install, add the following to a file in the root of your repository `.pre-commit-config.yaml`, and run `pre-commit install`

A example below.  This runs the kustomize_build pre-commit hook, only for folders in the `k8s/` folder, with the optional 'dry-run' step in server mode.

```yaml
  - repo: https://github.com/Truxnell/pre-commit
    rev: v0.0.9
    hooks:
      - id: kustomize_build
        files: ^k8s/
        args: [--dry-run=server]
```

This hook will then run each push.

## Hooks

### kustomize_build

This hook will scan each yaml file in the folder, and check if that folder has a valid kustomization file.  If it finds one, it will run `kustomize build .` on that path to check the kustomization will build, with any changes you have made.

Note: This hook works best with the practice of having a kustomize in a folder, with its yaml in the same folder.  The value of this hook diminishes if kustomize are calling in different folders, as this hook cannot calculate the multitute of links a kustomize could have.

This hook can optionally run `kubectl dry-run` on the resulting build kustomize, for additional vaidation.  This can be run in two modes:

* --dry-run=client - A basic validation that the parsed YAML file(s) are valid against basic schema.
* --dry-run=server - A powerful validation that connects to your cluster and validates that the server could apply the file.  This is increidbly powerful, as it will reject invalid namespaces,

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

* **kustomize-build** - Ensure modified kustomize files render, and optionally validate with `kubectl --dry-run`

## Planned

* **helm-release-lint** - Lint a helm release file with values in file
* **kubeconform-lint** - Lint each yaml with kubeconform
