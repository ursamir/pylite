from setuptools import setup, find_packages
setup(
    name='pylite',
    version='0.1.0',
    author='ursamir',
    author_email='samir.nmiet@gmail.com',
    description='A minimal lightweight-charts PySide6 wrapper',
    packages=find_packages(),
    install_requires=[
        "PySide6",
        "PyQtWebEngine"
    ],
    package_data={
        'pylite': ['scripts/*'],
    },
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)