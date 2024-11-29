from setuptools import setup, find_packages

setup(
    name="py_gfxhelper_lib",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["fastapi==0.115.5", "tinydb==4.8.2"],
)
