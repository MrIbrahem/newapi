"""

from newapi.except_err import exception_err, warn_err

"""
import inspect
import traceback
from warnings import warn
import pywikibot


def warn_err(err):
    """
    Return formatted warning message with error details.
    """
    err = str(err)
    nn = inspect.stack()[2][3]
    return f"\ndef {nn}(): {err}"


def exception_err(e, text=""):
    # pywikibot.output("====")
    pywikibot.output("<<red>>Traceback (most recent call last):")
    warn(warn_err(f"Exception:{str(e)}"), UserWarning, stacklevel=3)
    pywikibot.output(text)
    # ---
    err = traceback.format_exc(limit=2)
    err = str(err).replace("Traceback (most recent call last):", "").strip()
    # ---
    pywikibot.output(err)
    pywikibot.output("CRITICAL:")
    # pywikibot.output("====")
