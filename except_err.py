"""

python3 bots/new/newapi/except_err.py
tfj run exc1 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py newapi/except_err"

from newapi.except_err import exception_err
from newapi.except_err import exception_err, warn_err

"""
import inspect
import traceback
from warnings import warn

try:
    from . import printe
except:
    import printe


def warn_err(err):
    """
    Return formatted warning message with error details.
    """
    err = str(err)
    nn = inspect.stack()[2][3]
    return f"\ndef {nn}(): {err}"


def exception_err(e, text=""):
    # ---
    if not isinstance(text, str):
        text = str(text)
    # ---
    printe.output("<<yellow>> start exception_err:")
    # ---
    printe.error("Traceback (most recent call last):")
    warn(warn_err(f"Exception:{str(e)}"), UserWarning, stacklevel=3)
    printe.warn(text)
    # ---
    err = traceback.format_exc(limit=2)
    err = str(err).replace("Traceback (most recent call last):", "").strip()
    # ---
    printe.warn(err)
    printe.warn("CRITICAL:")
    # printe.info("====")


if __name__ == "__main__":

    def xx(t, x):
        exception_err(t, x)

    xx("Exception", "test!!")
