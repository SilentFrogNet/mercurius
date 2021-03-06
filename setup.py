import os
import setuptools

SHORT_DESCRIPTION = "A tool to extract and manage medatada from remote domains or locally."

with open("README.md", 'r') as f:
    LONG_DESCRIPTION = f.read()

with open("VERSION", 'r') as f:
    __version__ = f.read().strip()

# hacky and ugly workaround to get all dependecies installed.
# TODO: remove it in future releases
os.system('pip install git+git://github.com/SilentFrogNet/spinner.git')
os.system('pip install git+git://github.com/SilentFrogNet/click-shell.git')

setuptools.setup(
    name="mercurius",
    version=__version__,
    author="Ilario Dal Grande",
    author_email="ilario.dalgrande@silentfrog.net",
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license='GPLv2',
    url="https://github.com/SilentFrogNet/mercurius",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Topic :: Security',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Utilities',
        'Topic :: System :: Shells',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only'
    ],
    install_requires=[
        'Click',
        'termcolor',
        'colorama',
        'configobj',
        'pdfminer.six',
        'hachoir3',
        'requests',
        'Pillow',
        'validators',
        'google',
        'pluggy',
        # 'spinner',
        # 'click-shell'
    ],
    dependency_links=[
        # 'git+https://github.com/SilentFrogNet/spinner.git#egg=spinner',
        # 'git+https://github.com/SilentFrogNet/click-shell.git#egg=click-shell',
    ],
    entry_points='''
        [console_scripts]
        merc=app:cli
    ''',
)
