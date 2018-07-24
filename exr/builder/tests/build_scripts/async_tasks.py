#!/usr/bin/python

from exr.builder import task, async_task
import threading
import time

tasks_run = []


@task()
def clean():
    print("clean ({})".format(threading.current_thread().getName()))
    tasks_run.append('clean')


@task(clean)
def html():
    print("html ({})".format(threading.current_thread().getName()))
    tasks_run.append('html')


@task()
def images():
    print("images ({})".format(threading.current_thread().getName()))
    tasks_run.append('images')


@async_task(clean)
def android():
    time.sleep(1)
    print("android ({})".format(threading.current_thread().getName()))
    tasks_run.append('android')


@async_task(clean)
def ios():
    time.sleep(5)
    print("ios ({})".format(threading.current_thread().getName()))
    tasks_run.append('ios')


@task(html, images, ios, android)
def build_all():
    tasks_run.append('build_all')
    pass


def some_utility_method():
    """Some utility method."""

    print("some utility method")


__DEFAULT__ = build_all
