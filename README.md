# Saar 

![alt text](https://github.com/bgrsmn/saar/blob/92352400e0a51b567a4de25bcd053ede03c478da/favicon.png "Logo Title Text 1")

##### Siem Auto Add Rule

1. [Code Description](https://github.com/bgrsmn/saar#code-description#codedescription)
2. [Tech](https://github.com/bgrsmn/saar#tech)
3. [Installation](https://github.com/bgrsmn/saar#installation)
4. [Usage](https://github.com/bgrsmn/saar#usage)
5. [To Do](https://github.com/bgrsmn/saar#to-do)
6. [Usage](https://github.com/bgrsmn/saar#usage)
7. [License](https://github.com/bgrsmn/saar#license)

## Code Description

This project helps you manage the rules in a Siem product in a more organized way. By categorizing the rules, you can keep track of them more easily. In addition, it enables the addition of correlation rules with their categories to your Siem product, making it easier to view the added rules in the Siem web interface and speeding up your workflow.

## Tech

Saar uses a number of open source projects to work properly:

- [Python] - Python is a computer programming language often used to build websites and software, automate tasks, and conduct data analysis!
- [Bash Script] - A bash script is a file containing a sequence of commands that are executed by the bash program line by line. 
- [Visual Studio Code] - Visual Studio Code is a source-code editor that can be used with a variety of programming languages, including C, C#, C++, Fortran, Go, Java, JavaScript, Node.js, Python, Rust.

And of course saar itself is open source with a [public repository][bgrsmn] on GitHub.

## Installation

You can manually download the required libraries for the code to run or use the `python_venv.sh` script to run it in an isolated environment.

```sh
bash python_venv.sh
```

```sh
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
```

## Usage

To successfully run the code, you need to run the  `saar.py` file first, which enables the addition of correlation rules with their categories to your Siem product. You need to specify the path of the venv file that you run in an isolated environment to perform this operation. For example, it can be specified as  `/root/venv/bin/python3 saar.py`

First Tab:
```sh
python3 saar.py
```

After successfully running the code, the   `clean_sıem.sh` script can be used to view the rules in the Siem web interface. This script checks whether the rules have been added or not by entering the Siem web interface after the relevant workers have performed the truncate operation. To use this script, the   `bash clean_sıem.sh` command can be used.

Second Tab:

```sh
bash clean_sıem.sh
```

```sh
#!/bin/bash

# Stop cryptosimpir service
sudo systemctl stop cryptosimpir
# Stop pirweb service
sudo systemctl stop pirweb

# Kill mono, dotnet and LOGCACHE processes
sudo pkill -f -9 mono
sudo pkill -f -9 dotnet
sudo pkill -f -9 LOGCACHE

# Connect to MySQL and truncate tables
sudo mysql -u(username) -p -e "use cryptosimpir; truncate pir_jobs; truncate pir_jobcancelrequests; truncate pir_currentmasters; truncate pir_currentmasterscandidates;"

# Start pirweb and cryptosimpir services
sudo systemctl start pirweb
sudo systemctl start cryptosimpir
```


Finally, you can see that the rules have been added when you log in to the SIEM web interface through the CLI `iisreset` as an administrator on your windows machine.

(requisite) Third:

```sh
iisreset
```

## To Do

For production release:

- In future versions, a feature can be added to automatically download the libraries.
- To make the code more user-friendly, a command-line interface can be added.

## License

MIT

**Free Software, Hell Yeah!**



   [bgrsmn]: <https://github.com/bgrsmn?tab=repositories>
   [git-repo-url]: <https://github.com/bgrsmn?tab=repositories>
   [python]: <https://www.python.org/download/releases/3.0/>
   [bash script]: <https://ryanstutorials.net/bash-scripting-tutorial/bash-script.php>
   [visual studio code]: <https://code.visualstudio.com>


