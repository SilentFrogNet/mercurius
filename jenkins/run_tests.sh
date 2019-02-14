PYENV_HOME=$WORKSPACE/.pyenv/

# Delete previously built virtualenv
if [ -d $PYENV_HOME ]; then
    rm -rf $PYENV_HOME
fi

# Create virtualenv and install necessary packages
python -m venv $PYENV_HOME	# try to use python's builtin venv
. $PYENV_HOME/bin/activate
pip install --quiet --upgrade pip
pip install --quiet pycryptodome
pip install --quiet pylint
pip install --quiet pytest
pip install --quiet pytest-cov
pip install --quiet -e $WORKSPACE/  # where your setup.py lives
py.test --verbose --cov=mercurius --cov-report=xml:test-reports/coverage-results.xml --junit-xml test-reports/results.xml mercurius/tests
pylint -f parseable --exit-zero mercurius/ | tee test-reports/pylint.out
