"""

python3 core8/pwb.py newapi/tests/test_page ask

python3 core8/pwb.py newapi/tests/test_page

"""
from newapi.page import MainPage

# ---
# page = MainPage("فريدريش تسيمرمان", 'ar')
page = MainPage("وب:ملعب", "ar")
# ---
"""
exists	  = page.exists()
if not exists: return
# ---
page_edit = page.can_edit()
if not page_edit: return
# ---
if page.isRedirect() :	return
# target = page.get_redirect_target()
# ---
text	    = page.get_text()
ns		    = page.namespace()
links	    = page.page_links()
categories  = page.get_categories(with_hidden=False)
langlinks   = page.get_langlinks()
back_links  = page.page_backlinks()
wiki_links  = page.get_wiki_links_from_text()
words	    = page.get_words()
templates   = page.get_templates()
save_page   = page.save(newtext='', summary='', nocreate=1, minor='')
create	    = page.Create(text='', summary='')
# ---
text_html   = page.get_text_html()
hidden_categories= page.get_hidden_categories()
flagged     = page.is_flagged()
timestamp   = page.get_timestamp()
user	    = page.get_user()
purge	    = page.purge()
"""

# ---
text = page.get_text()
print(text)
# ---
ex = page.get_wiki_links_from_text()
print("---------------------------")
print(f"get_wiki_links_from_text:{ex}")
# ---
hidden_categories = page.get_hidden_categories()
print("---------------------------")
print(f"hidden_categories:{hidden_categories}")
# ---
newtext = "تجربة!\n" * 5
# ---
save = page.save(newtext=newtext)
# ---
