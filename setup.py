from setuptools import find_packages, setup

setup(
    name="kustomize_build",
    description="Test kustomize build on kustomize files",
    url="https://github.com/Truxnell/pre-commit",
    version="0.0.1",
    author="Nat Allan",
    author_email="nat@natallan.com",
    platforms="linux",
    install_requires=["kustomize"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    packages=find_packages("."),
    entry_points={
        "console_scripts": [
            "kustomize_build=hooks.kustomize_build:main",
        ],
    },
)
