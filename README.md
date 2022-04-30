# Pre-commit hooks

This is a WIP repository for a few plannet pre-commit hooks.  These are aimed to make life easier with using k8s in a gitops fashion.

## Planned

* **helm-release-lint** - Lint a helm release file with values in file
* **kustomize-render** - Ensure modified kustomize files render
* **kubeval-dryrun** - Apply each yaml manifest with `kubeval --dry-run=server` to ensure file will apply to server
* **kubeconform-lint** - Lint each yaml with kubeconform
