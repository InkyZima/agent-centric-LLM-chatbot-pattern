import time

def delay4(func):
  """
  Delays the execution of a function to approximately 5 seconds.

  Args:
    func: The function to be delayed.

  Returns:
    The result of the input function.
  """
  def delayed_func(*args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    sleep_duration = max(0, 4 - execution_time) # Ensure sleep is not negative
    time.sleep(sleep_duration)
    return result
  return delayed_func

def delay8(func):
  """
  Delays the execution of a function to approximately 5 seconds.

  Args:
    func: The function to be delayed.

  Returns:
    The result of the input function.
  """
  def delayed_func(*args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    sleep_duration = max(0, 8 - execution_time) # Ensure sleep is not negative
    time.sleep(sleep_duration)
    return result
  return delayed_func