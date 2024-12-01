from setuptools import setup, find_packages

setup(
    name="py_gfxhelper_lib",
    version="0.0.1",
    package_dir={"": "src"},
    author="Timur Timaev",
    license="MIT",
    packages=find_packages(where="src"),
    install_requires=["fastapi", "tinydb", "httpx"],
    python_requires=">=3.10",
)
