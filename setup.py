from setuptools import setup, find_packages


setup(
    name="MathStuff",
    version="0.0.1",
    description="Math Stuff",
    long_description="Math Stuff",
    url="https://github.com/Vipul-Cariappa/Math-Stuff",
    author="Vipul Cariappa",
    author_email="vipulcariappa@gmail.com",
    license="MIT",
    packages=find_packages(".", exclude=["tests/"]),
    install_requires=[
        "contourpy==1.0.7",
        "cycler==0.11.0",
        "fonttools==4.38.0",
        "kiwisolver==1.4.4",
        "matplotlib==3.6.3",
        "mpmath==1.2.1",
        "numpy==1.24.1",
        "packaging==23.0",
        "Pillow==9.4.0",
        "pyparsing==3.0.9",
        "python-dateutil==2.8.2",
        "six==1.16.0",
        "sympy==1.11.1",
    ],
)
