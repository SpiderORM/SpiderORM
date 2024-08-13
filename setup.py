from setuptools import setup, find_packages

setup(
    name="spider-orm",
    version="0.1.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'mysqlclient',
        'sqlite3',  
    ],
    extras_require={
        'dev': [
            'pytest>=3.7',
            'sphinx',
            'pytest-mock',  
            'coverage',     
        ],
    },
    author="Simão Domingos de Oliveira António",
    author_email="simaodomingos413@gmail.com",
    description="Spider-ORM is a lightweight and flexible ORM (Object-Relational Mapping) library for Python.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://spider-orm.netlify.app/',
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
