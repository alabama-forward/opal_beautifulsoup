from setuptools import setup, find_packages

setup(
    name="opal",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "selenium>=4.0.0",
        "webdriver-manager>=4.0.0",
        "pytest"
    ],
    entry_points={
        'console_scripts': [
            'opal=opal.main:main',
        ],
    },
    author="Gabriel Cabán Cubero",
    author_email="gabri@alforward.org",
    description="OPAL - Oppositional Positions in Alabama: Web scraper for Alabama news sites and court records",
    keywords="news, parser, web-scraping, court-records, alabama",
    python_requires=">=3.6",
    url="https://github.com/alabamaforward/opal",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)