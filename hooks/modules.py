import yaml
from yaml.loader import SafeLoader


def is_k8s_manifest(filename):

    file = open(filename)
    data = yaml.load_all(file, Loader=SafeLoader)
    try:
        for f in data:
            if not f.get("apiVersion", False) or not f.get("kind", False):
                return 0
    except:
        return 0

    return 1
