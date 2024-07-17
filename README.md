Python module for Wikimedia API:

### Login.

```` python
from newapi import super_login

bot   = Login(lang, family='wikipedia')
# ---
bot.add_User_tables('wikipedia', {'username': '', 'password': ''})
login = bot.log_to_wiki_1()
json1 = bot.post(params, Type='post', addtoken=False)
````
### Pages.

```` python
# ---
from newapi.page import MainPage
page      = MainPage(title, 'ar', family='wikipedia')
# ---
exists    = page.exists()
if not exists: return
# ---
page_edit = page.can_edit(script='')
if not page_edit: return
# ---
if page.isRedirect() :  return
if page.isDisambiguation() :  return
# target = page.get_redirect_target()
# ---
text        = page.get_text()
ns          = page.namespace()
links       = page.page_links()
categories  = page.get_categories(with_hidden=False)
langlinks   = page.get_langlinks()
wiki_links  = page.get_wiki_links_from_text()
refs        = page.Get_tags(tag='ref')# for x in ref: name, contents = x.name, x.contents
words       = page.get_words()
templates   = page.get_templates()
temps_API   = page.get_templates_API()
save_page   = page.save(newtext='', summary='', nocreate=1, minor='')
create      = page.Create(text='', summary='')
# ---
extlinks    = page.get_extlinks()
back_links  = page.page_backlinks()
text_html   = page.get_text_html()
hidden_categories= page.get_hidden_categories()
flagged     = page.is_flagged()
timestamp   = page.get_timestamp()
user        = page.get_user()
userinfo    = page.get_userinfo() # "id", "name", "groups"
revisions   = page.get_revisions(rvprops=['content'])
purge       = page.purge()
````

### Categories.

```` python
from newapi.page import CatDepth
cat_members = CatDepth(title, sitecode='en', family="wikipedia", depth=0, ns="all", nslist=[], tempyes=[])
````
### Templates.

```` python

````
### API Actions.

```` python
from newapi.page import NEW_API
api_new  = NEW_API('www', family='nccommons')
login    = api_new.Login_to_wiki()
json1    = api_new.post_params(params, addtoken=False)
pages    = api_new.Find_pages_exists_or_not(liste)
pages    = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)
search   = api_new.Search(value='', ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
newpages = api_new.Get_Newpages(limit="max", namespace="0", rcstart="", user='', three_houers=False)
usercont = api_new.UserContribs(user, limit=5000, namespace="*", ucshow="")
l_links  = api_new.Get_langlinks_for_list(titles, targtsitecode="", numbes=50)
text_w   = api_new.expandtemplates(text)
subst    = api_new.Parse_Text('{{subst:page_name}}', title)
extlinks = api_new.get_extlinks(title)
revisions= api_new.get_revisions(title)

````

