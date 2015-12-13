def log_msg(func):
  def with_logging(*arg, **kwargs):
    print(func.__name__ + "...", end="", flush=True)
    res = func(*arg, **kwargs)
    print("done")

    return res

  return with_logging
