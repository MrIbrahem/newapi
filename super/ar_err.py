#!/usr/bin/python3

"""

from newapi.super.ar_err import find_edit_error
if find_edit_error(old, new): return 
"""

def find_edit_error(old, new):
  # Define the dictionary of conversion phrases
  conversion_phrases = {
    "#تحويل [["
  }

  for phrase in conversion_phrases:
    if phrase in old and phrase not in new:
      print(f"ar_err.py found ({phrase}) in old but bot in new. return True")
      return True

  return False
