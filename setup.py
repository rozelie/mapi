from distutils.core import setup
from pathlib import Path

requirements = Path("requirements.txt").read_text().splitlines()


setup(
    name="mapi",
    version="0.0.1",
    description="mapi",
    author="Ryan Ozelie",
    author_email="ryan.ozelie@gmail.com",
    url="https://github.com/rozelie/mapi",
    packages=["mapi"],
    install_requires=requirements,
)
