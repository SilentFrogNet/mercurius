PYENV_HOME=$WORKSPACE/.pyenv/

# Delete previously built virtualenv
if [ -d $PYENV_HOME ]; then
    rm -rf $PYENV_HOME
fi

# Create virtualenv and install necessary packages
python3 -m venv $PYENV_HOME	# try to use python's builtin venv
source $PYENV_HOME/bin/activate
pip3 install --quiet --upgrade pip
pip3 install --quiet pylint
pip3 install --quiet pytest
pip3 install --quiet $WORKSPACE/  # where your setup.py lives
py.test --verbose --junit-xml test-reports/results.xml mercurius/tests
# pylint -f parseable mercurius/ | tee pylint.out
