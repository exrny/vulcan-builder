import inspect
import time
import logging

class Task(object):

    def __init__(self, func, dependencies, options, **kwargs):
        """
        @type func: 0-ary function
        @type dependencies: list of Task objects
        """
        self.func = func
        self.name = func.__name__
        self.doc = inspect.getdoc(func) or ''
        self.dependencies = dependencies
        self.ignored = bool(options.get('ignore', False))
        self.async_task = kwargs.get('async_task', False)

    def __call__(self, *args, **kwargs):
        self.func.__call__(*args, **kwargs)

    @classmethod
    def is_task(cls, obj):
        """
        Returns true is an object is a build task.
        """
        return isinstance(obj, cls)


class CurrentThreadExecutor(object):
  
  def __init__(self):
      pass


  def submit(self, task, *args, **kwargs):
      try:
          # Run task.
          startTime = int(round(time.time() * 1000))
          task(*(args or []), **(kwargs or {}))
          stopTime = int(round(time.time() * 1000))
      except Exception:
          stopTime = int(round(time.time() * 1000))
          # logger.critical("Error in task \"%s\". Time: %s sec" % (
          #     task.name, (float(stopTime)-startTime)/1000))
          # logger.critical("Aborting build")
          raise

      # logger.info("Completed task \"%s\". Time: %s sec" %
      #             (task.name, (float(stopTime)-startTime)/1000))

      return PseudoFutureTask()      

class PseudoFutureTask(object):

  def __init__(self):
    pass

  def running(self):
    return False
