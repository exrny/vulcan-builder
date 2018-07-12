#!/usr/bin/python

from exr.builder import task, async_task
import threading
import time

tasks_run = []

@task()
def clean():
    tasks_run.append('clean')
    print("clean ({})".format(threading.current_thread().getName()))


@task(clean)
def html():
    tasks_run.append('html')
    print("html ({})".format(threading.current_thread().getName()))


@task()
def images():
    tasks_run.append('images')
    print("images ({})".format(threading.current_thread().getName()))


@async_task(clean)
def android():
    time.sleep(1)
    tasks_run.append('android')
    print("android ({})".format(threading.current_thread().getName()))


@async_task(clean)
def ios():
    time.sleep(3)
    tasks_run.append('ios')
    print("ios ({})".format(threading.current_thread().getName()))


@task(html, images, ios, android)
def build_all():
  tasks_run.append('build_all')
  pass

def some_utility_method():
    """Some utility method."""

    print("some utility method")


__DEFAULT__ = build_all
