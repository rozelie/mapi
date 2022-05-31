from pathlib import Path

from setuptools import find_packages, setup

requirements = Path("requirements.txt").read_text().splitlines()
dev_requirements = Path("dev_requirements.txt").read_text().splitlines()


setup(
    name="mapi",
    version="0.0.1",
    description="mapi",
    author="Ryan Ozelie",
    author_email="ryan.ozelie@gmail.com",
    url="https://github.com/rozelie/mapi",
    packages=find_packages(".", exclude=["tests"]),
    package_dir={"": "."},
    include_package_data=True,
    install_requires=requirements,
    tests_requires=dev_requirements,
)
