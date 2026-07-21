from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='tisk',
    version='0.1.1',
    description='Simple but cool Task manager',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['rich'],
    author='Timothy Emad',
    entry_points={
        'console_scripts':[
            'tisk=tisk:main',
        ],
    },
)