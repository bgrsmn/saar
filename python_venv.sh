#! /bin/bash

yum install python3-venv
python3 -m venv venv
source venv/bin/activate
# Check you have an activated venv and you're in the right directory for it
if [[ $VIRTUAL_ENV == $PWD'/venv' ]]; then
    echo "Upgrading pip in present virtual environment"
    python3 -m pip install --upgrade pip
    echo "Installing requirements in present virtual environment"
    pip install python-dotenv
    pip install pylint
    pip install pymysql
else
    echo "
    ---------------------------------------------------------------------------------
        You need to have THIS directory's venv activated to install requirements!
        You are now in:    $PWD
    ---------------------------------------------------------------------------------
    "
fi
