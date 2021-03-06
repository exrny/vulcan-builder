#!/usr/bin/python

from vulcan.builder import task

from vulcan.builder.tests.build_scripts.build_with_params import *
from vulcan.builder.tests.build_scripts import build_with_params

tasks_run = []


@task()
def local_task():
    tasks_run.append('local_task')


@task(clean, html, local_task)
def task_with_imported_dependencies():
    tasks_run.append('task_with_imported_dependencies')


__DEFAULT__ = task_with_imported_dependencies
