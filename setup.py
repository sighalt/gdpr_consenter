from setuptools import setup, find_packages

setup(
    name="gdpr_consenter",
    packages=find_packages(),
    version="0.0.1",
    install_requires=[
        "selenium",
    ],
    entry_points={
        "console_scripts": [
            "gdpr-consenter = gdpr_consenter.__init__:main"
        ]
    },
)

