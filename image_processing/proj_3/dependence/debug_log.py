import time 

def log_msg(func):
  def with_logging(*arg, **kwargs):
    print(func.__name__ + "...", end="", flush=True)
    t0 = time.time()
    res = func(*arg, **kwargs)
    t1 = time.time()
    print("done  %.2g sec" % (t1 - t0))

    return res

  return with_logging
