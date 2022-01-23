from setuptools import setup

setup(
    name='veth',
    version='0.1.0',
    author='V',
    author_email='vds.avatar.seven@gmail.com',
    description='geth client tool',
    install_requires=[
        'Click',
        'web3',
        'kafka-python',

    ],
    entry_points={
        'console_scripts': [
            'veth=ETL.cli:cli'
        ]
    }
)
