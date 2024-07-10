from setuptools import setup, find_packages

setup(
    name='sc-tools',
    version='0.1.0', 
    description='Speedcubing Tools',
    url='https://github.com/vicalbiter/sc-tools.git',
    author='Vicente Albíter Alpízar',
    author_email='vic.albiter@gmail.com',
    packages=find_packages(exclude=['logs', 'notebooks']),
    install_requires=[
        'matplotlib~=3.5.3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
)