"""

"""
import sys
import wikitextparser as wtp
from pathlib import Path
import codecs

# ---
sys.argv.append('workibrahem')
sys.argv.append('ask')
# ---
# ---
# python3 core8/pwb.py newapi/pformat -title:قالب:Cycling_race/stageclassification3
# python3 core8/pwb.py newapi/pformat -title:قالب:
# python3 core8/pwb.py newapi/pformat -title:قالب:Interlanguage_link_multi
# python3 core8/pwb.py newapi/pformat -title:قالب:Cs1_wrapper


def make_new_text(text):
    # ---
    new_text = text
    # ---
    # Parse the wikitext
    temps = wtp.parse(text).templates
    # ---
    for temp in temps:
        temp_text = temp.string
        new_temp = temp.pformat()
        new_text = new_text.replace(temp_text, new_temp)
    # ---
    return new_text


# ---
Dir = Path(__file__).parent
# ---
title = ''
text = (Dir / "pformat.txt").read_text(encoding="utf-8")
for arg in sys.argv:
    arg, _, value = arg.partition(':')
    if arg == '-title' or arg == '-page':
        title = value
# ---
if title != '':
    # ---
    from newapi.page import MainPage

    page = MainPage(title, 'ar', family='wikipedia')
    text = page.get_text()
    newtext = make_new_text(text)
    if 'save' in sys.argv:
        save_page = page.save(newtext=newtext, summary='', nocreate=1, minor='')
else:
    prased = wtp.parse(text)
    newtext = prased.pformat()
# ---
print(newtext)
# ---
with (Dir / "pformat.txt").open("w", encoding="utf-8") as logfile:
    logfile.write(newtext)
# ---
print('add "save" to sys.argv to save.')
# ---
