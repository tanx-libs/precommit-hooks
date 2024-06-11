from setuptools import setup, find_packages

setup(
    name='pre-commit-hooks',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pre-commit',
    ],
    entry_points={
        'console_scripts': [
            'private_key_check = private_key_check:main',
        ],
    },
)
