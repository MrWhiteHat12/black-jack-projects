import threading
import builtins

# Capture the original print function at import time so the wrapper can call
# it even if callers reassign builtins.print to this safe wrapper later on.
_original_print = builtins.print
_print_lock = threading.Lock()


def safe_print(*args, **kwargs):
    """Thread-safe print wrapper. Acquires a lock to prevent concurrent writes
    from multiple threads interleaving on the console."""
    with _print_lock:
        _original_print(*args, **kwargs)
