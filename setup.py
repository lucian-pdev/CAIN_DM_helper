from setuptools import setup, find_packages

setup(
    name="cain-helper",
    version="0.1.0",
    py_modules=["cain_helper"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cain-helper = cain_helper:main",
        ]
    },
    install_requires=[
        # any deps like click or tabulate if you add them later
    ],
    author="HowelBane",
    license="MIT",
    description="Terminal GM helper for the CAIN RPG",
)
