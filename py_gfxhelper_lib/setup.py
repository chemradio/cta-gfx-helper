from setuptools import setup, find_packages

setup(
    name="py_gfxhelper_lib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["fastapi==0.115.5", "tinydb==4.8.2"],
)
