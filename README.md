Sc_Py-Sergi-Lluis
===

One paragraph of project description goes here

---

# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

We will need **Python3** to run the code and **pip3** to install required libraries

> for Ubuntu:
```
$ sudo apt install -y python3 python3-pip
```

Install Supercollider

> for Ubuntu:
```
$ sudo apt install -y supercollider
```

## Download/Clone Repo

To your projects folder:

```
$ cd $HOME/Workspace
$ git clone git@github.com:SergiA07/Sc_Py-Sergi-Lluis.git
$ cd Sc_Py-Sergi-Lluis
```

## Setup Python Virtual Environment

Use the package manager **pip** to install virtualenv and virtualenvwrapper (_pip_ or _pip3_, both are fine)

> for Ubuntu:
```
$ pip install virtualenv virtualenvwrapper
```

### Shell Startup File

Add three lines to your shell startup file (.bashrc, .profile, etc.) to set: 
  
  * The location where the virtual environments should live.
  * The location of your development project directories -- Adjust to your needs
  * And the location of the script installed with virtualenvwrapper package

> For Ubuntu:
```
$ export WORKON_HOME=$HOME/.virtualenvs
$ export PROJECT_HOME=$HOME/Workspace
$ source /usr/local/bin/virtualenvwrapper.sh
```

### Create Virtual Environment

Using the **mkvirtualenv** tool provided by **virtualenvwrapper** create a new virtual environment:

  * Link this _venv_ to the project with the -a flag
  * Install dependencies by referencing the _requirements.txt_ file contained in the project
  * Set the Python interpreter version
  
> For Ubuntu:
```
$ mkvirtualenv --help
Usage: mkvirtualenv [-a project_path] [-i package] [-r requirements_file] [virtualenv options] env_name

$ mkvirtualenv -a $HOME/Workspace/Sc_Py-Sergi-Lluis/ -r $HOME/Workspace/Sc_Py-Sergi-Lluis/requirements.txt --python=python3 collider
```

### Activate/Deactivate Virtual Environment

To activate a virtual environment and change the current working directory to the project directory execute `workon env_name`. In order to deactivate the virtual environment just execute `deactivate`.

Check the [Command Reference](https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html) for additional commands and options for working with virtual environments.