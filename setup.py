import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

with open("VERSION", 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="Mercurius",
    description="A tool to extract and manage medatada from remote domains or locally.",
    version=version,
    author="Ilario Dal Grande",
    author_email="ilario.dalgrande@silentfrog.net",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SilentFrogNet/mercurius",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        merc=mercurius_click:cli
    ''',
)
