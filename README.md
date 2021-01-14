# Planka Import Utility #

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0%201.0-green.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

A python utility to import a structured JSON file into [Planka](https://planka.app/)

## Functions ##
 
This utility is currently in the pre-Alpha stages with significant limitations. However, creating a new project with pre-defined boards, lists, cards, and tasks works.  The functionality to load into a previously created project does not currently work as it is designed with a specific project in mind. Future evolution to the Alpha stage will allow this to work on any projects with a structured JSON file. 

## Scripts ##

`planka-import` provides the following options:  
* `--load` - When provided a project name and json file, a new project is created and populated form the json.  
* `--new` - **LIMITED FUNCTIONALITY** When provided a project name and json file, a project will be populated from the json file.  
* `--template` - **KNOW BUG** When provided a project name, a json file is produced to be used as a template for the other options.  

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

Build `planka-utility` from source:

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
