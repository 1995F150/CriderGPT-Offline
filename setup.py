from setuptools import setup, find_packages

setup(
name="CriderGPT-Offline",
version="1.0.0",
author="Jessie Crider (CriderGPT)",
author_email="support@cridergpt.com",
description="Standalone offline version of CriderGPT — Smarter Tech for Stronger Farms.",
long_description=open("README.md", "r", encoding="utf-8").read(),
long_description_content_type="text/markdown",
url="https://github.com/1995F150/CriderGPT-Offline",
packages=find_packages(),
install_requires=[
"PyQt5",
"Flask",
"torch",
"transformers",
"pillow",
"numpy",
],
classifiers=[
"Programming Language :: Python :: 3",
"Operating System :: Microsoft :: Windows",
],
python_requires=">=3.8",
)
