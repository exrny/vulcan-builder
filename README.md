[![Build Status](https://travis-ci.org/exrny/vulcan-builder.png?branch=master)](https://travis-ci.org/exrny/vulcan-builder)

Vulcan Builder
===========

This project is a fork of Pynt by [Raghunandan Rao](https://github.com/rags/pynt). We will contribute changes to the original rags/pynt repo.

Vulcan Builder supports EXR’s applications via a lightweight, concise Python DevOps tool. We will develop our own improvements on the initial rags/pynt repo here and publish improvements to the original repo.

This is an EXR Open Source project.

A pynt of Python build. 
=======================

## Features

* Easy to learn.
* Build tasks are just python funtions.
* Manages dependencies between tasks.
* Automatically generates a command line interface.
* Rake style param passing to tasks
* Supports python 2.7 and python 3.x
* Async tasks

## Todo Features

* Additional tasks timing reporting 
* Debug mode

## Installation


You can install vulcan-builder from the Python Package Index (PyPI) or from source.

Using pip

```bash
$ pip install vulcan-builder
```

Using easy_install

```bash
$ easy_install vulcan-builder
```

## Example


The build script is written in pure Python and vulcan-builder takes care of managing
any dependencies between tasks and generating a command line interface.

Writing build tasks is really simple, all you need to know is the @task decorator. Tasks are just regular Python 
functions marked with the ``@task()`` decorator. Dependencies are specified with ``@task()`` too. Tasks can be 
ignored with the ``@task(ignore=True)``. Disabling a task is an useful feature to have in situations where you have one
task that a lot of other tasks depend on and you want to quickly remove it from the dependency chains of all the 
dependent tasks. 

**build.py**
------------

```python

#!/usr/bin/python

import sys
from vulcan.builder import task

@task()
def clean():
    '''Clean build directory.'''
    print 'Cleaning build directory...'

@task(clean)
def html(target='.'):
    '''Generate HTML.'''
    print 'Generating HTML in directory "%s"' %  target

@task(clean, ignore=True)
def images():
    '''Prepare images.'''
    print 'Preparing images...'

@task(html,images)
def start_server(server='localhost', port = '80'):
    '''Start the server'''
    print 'Starting server at %s:%s' % (server, port)

@task(start_server) #Depends on task with all optional params
def stop_server():
    print 'Stopping server....'

@task()
def copy_file(src, dest):
    print 'Copying from %s to %s' % (src, dest)

@task()
def echo(*args,**kwargs):
    print args
    print kwargs
    
# Default task (if specified) is run when no task is specified in the command line
# make sure you define the variable __DEFAULT__ after the task is defined
# A good convention is to define it at the end of the module
# __DEFAULT__ is an optional member

__DEFAULT__=start_server
```

**Running vulcan-builder tasks**
-----------------------

The command line interface and help is automatically generated. Task descriptions
are extracted from function docstrings.

```bash
$ vb -h
usage: vb [-h] [-l] [-v] [-f file] [task [task ...]]

positional arguments:
  task                  perform specified task and all its dependencies

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-tasks      List the tasks
  -v, --version         Display the version information
  -f file, --file file  Build file to read the tasks from. Default is
                        'build.py'
```

```bash
$ vb -l
Tasks in build file ./build.py:
  clean                       Clean build directory.
  copy_file                   
  echo                        
  html                        Generate HTML.
  images           [Ignored]  Prepare images.
  start_server     [Default]  Start the server
  stop_server                 

Powered by vulcan-builder - A Lightweight Python Build Tool.
```
          
vulcan-builder takes care of dependencies between tasks. In the following case start_server depends on clean, html and image generation (image task is ignored).

```bash
$ vb #Runs the default task start_server. It does exactly what "vb start_server" would do.
[ example.py - Starting task "clean" ]
Cleaning build directory...
[ example.py - Completed task "clean" ]
[ example.py - Starting task "html" ]
Generating HTML in directory "."
[ example.py - Completed task "html" ]
[ example.py - Ignoring task "images" ]
[ example.py - Starting task "start_server" ]
Starting server at localhost:80
[ example.py - Completed task "start_server" ]
```

The first few characters of the task name is enough to execute the task, as long as the partial name is unambigious. You can specify multiple tasks to run in the commandline. Again the dependencies are taken taken care of.

```bash
$ vb cle ht cl
[ example.py - Starting task "clean" ]
Cleaning build directory...
[ example.py - Completed task "clean" ]
[ example.py - Starting task "html" ]
Generating HTML in directory "."
[ example.py - Completed task "html" ]
[ example.py - Starting task "clean" ]
Cleaning build directory...
[ example.py - Completed task "clean" ]
```

The 'html' task dependency 'clean' is run only once. But clean can be explicitly run again later.

vb tasks can accept parameters from commandline.

```bash
$ vb "copy_file[/path/to/foo, path_to_bar]"
[ example.py - Starting task "clean" ]
Cleaning build directory...
[ example.py - Completed task "clean" ]
[ example.py - Starting task "copy_file" ]
Copying from /path/to/foo to path_to_bar
[ example.py - Completed task "copy_file" ]
```

vb can also accept keyword arguments.

```bash
$ vb start[port=8888]
[ example.py - Starting task "clean" ]
Cleaning build directory...
[ example.py - Completed task "clean" ]
[ example.py - Starting task "html" ]
Generating HTML in directory "."
[ example.py - Completed task "html" ]
[ example.py - Ignoring task "images" ]
[ example.py - Starting task "start_server" ]
Starting server at localhost:8888
[ example.py - Completed task "start_server" ]
    
$ vb echo[hello,world,foo=bar,blah=123]
[ example.py - Starting task "echo" ]
('hello', 'world')
{'blah': '123', 'foo': 'bar'}
[ example.py - Completed task "echo" ]
```

**Organizing build scripts**
-----------------------------

You can break up your build files into modules and simple import them into your main build file.

```python
from deploy_tasks import *
from test_tasks import functional_tests, report_coverage
```

## Contributors/Contributing


* Raghunandan Rao - vulcan-builder is preceded by and forked from [pynt](https://github.com/rags/pynt), which was created by [Raghunandan Rao](https://github.com/rags/pynt).
* Calum J. Eadie - pynt is preceded by and forked from [microbuild](https://github.com/CalumJEadie/microbuild), which was created by [Calum J. Eadie](https://github.com/CalumJEadie).


If you want to make changes the repo is at https://github.com/exrny/vulcan-builder. You will need [pytest](http://www.pytest.org) to run the tests

```bash
$ ./vb t
```

It will be great if you can raise a [pull request](https://help.github.com/articles/using-pull-requests) once you are done.

If you find any bugs or need new features please raise a ticket in the [issues section](https://github.com/exrny/vulcan-builder/issues) of the github repo.
    
## License

vulcan-builder is licensed under a [MIT license](http://opensource.org/licenses/MIT)
