from setuptools import setup, find_packages

setup(
    name="opal",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pytest"
    ],
    entry_points={
        'console_scripts': [
            'opal=opal.main:main',
        ],
    },
    author="Gabriel Cabán Cubero",
    author_email="cabancubero@gmail.com",
    description="OPAL - Opposing Positions and Lingo Parser",
    keywords="news, parser, web-scraping",
    python_requires=">=3.6",
)