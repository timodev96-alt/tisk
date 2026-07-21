from setuptools import setup

setup(
    name='tisk',
    version='0.1.0',
    description='Simple but cool Task manager',
    install_requires=['tabulate'],
    author='Timothy Emad',
    entry_points={
        'console_scripts':[
            'tisk=tisk:main',
        ],
    },
)