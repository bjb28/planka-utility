# Planka Import Utility #

![Docker Pulls](https://img.shields.io/docker/pulls/bjb28/planka-utility) ![GitHub](https://img.shields.io/github/license/bjb28/planka-utility)
[![Coverage Status](https://coveralls.io/repos/github/bjb28/planka-utility/badge.svg?branch=main)](https://coveralls.io/github/bjb28/planka-utility?branch=main)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/bjb28/planka-utility.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/bjb28/planka-utility/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/bjb28/planka-utility.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/bjb28/planka-utility/context:python)

A python utility to import a structured JSON file into [Planka](https://planka.app/)

## Functions ##
 
This utility is currently in the pre-Alpha stages with significant limitations. However, creating a new project with pre-defined boards, lists, cards, and tasks works.  The functionality to load cards into a previously created project works as long as there are currently no cards in that specific list. 

## Scripts ##

`planka-import` provides the following options:  
* `--load` - When provided a project name and JSON file, a new project is created and populated form the JSON.  
* `--new` - When provided a project name and JSON file, a project will be updated to include the JSON file.  
* `--template` - **KNOWN BUG** When provided a project name, a JSON file is produced to be used as a template for the other options.  

## Usage ##

The script in this project can be executed either in a local Python environment or in a Docker container.

To install the scripts in your local Python environment:

```console
git clone https://github.com/bjb28/planka-utility.git
cd planka-utility
pip install --requirement requirements.txt
```

After the scripts have been installed, they can be run like any other script:

```console
planka-import
```

### Pull or build Docker image ###

Pull `bjb28/planka-utility` from the Docker repository:

```console
docker pull bjb28/planka-utility
```

Or build `planka-utility` from source:

```console
git clone https://github.com/bjb28/planka-utility.git
cd planka-utility
docker build --tag planka-utility .
```

### Run scripts via Docker ###

The easiest way to use the containerized scripts is to alias them in your
local shell:

```console
eval "$(docker run planka-utility)"
```

That will add aliases to your **current shell** for all of the
[scripts](#scripts) mentioned above, plus an additional one for
`planka-utility-bash`, which can be used to start up a `bash` shell inside
a `planka-utility` container.

## License ##

This is [CC0 1.0 Universal](https://github.com/bjb28/planka-utility/blob/main/LICENSE)
