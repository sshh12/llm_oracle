from typing import Callable, Any, Optional
import datetime
import hashlib
import pickle
import re
import os

MAX_CACHE_VAL_LEN = 20

cache_options = dict(cache=True, cache_dir="cache")


def cache_func(func: Callable) -> Callable:
    """
    Basic cache to save $$$ on API calls.

    Caches based on `str` and `int` args only. Cache is done only for a single calendar day.
    """

    def wrap(*args, **kwargs):
        os.makedirs(cache_options["cache_dir"], exist_ok=True)
        args = [*args] + list(kwargs.values())
        cache_val = re.sub("[^\w\d]", "", repr([arg for arg in args if isinstance(arg, str) or isinstance(arg, int)]))
        if len(cache_val) > MAX_CACHE_VAL_LEN:
            cache_val = str(int(hashlib.md5(cache_val.encode("utf-8")).hexdigest(), 16))
        date_key = datetime.datetime.now().isoformat()[:10].replace("-", "_")
        cache_key = f"{func.__name__}_{date_key}_{cache_val}"
        cache_fn = os.path.join(cache_options["cache_dir"], cache_key)
        if os.path.exists(cache_fn) and cache_options["cache"]:
            with open(cache_fn, "rb") as f:
                return pickle.load(f)
        else:
            result = func(*args, **kwargs)
            with open(cache_fn, "wb") as f:
                pickle.dump(result, f)
            return result

    return wrap


def run_with_retries(func: Callable, default_val: Optional[Any] = None, retries: Optional[int] = 3) -> Any:
    attempts = 0
    while True:
        try:
            attempts += 1
            return func()
        except Exception as e:
            print("run_with_retries", func, e)
            if attempts > retries:
                break
    return default_val
