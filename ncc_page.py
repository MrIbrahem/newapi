# ---
"""
from newapi.ncc_page import CatDepth, CatDepthLogin
# CatDepthLogin(sitecode="www", family="nccommons")
# cat_members = CatDepth(title, sitecode='www', family="nccommons", depth=0, ns=10, nslist=[], onlyns=False, tempyes=[])

from newapi.ncc_page import MainPage as ncc_MainPage
'''
page      = ncc_MainPage(title, 'www', family='nccommons')
exists    = page.exists()
if not exists: return
# ---
page_edit = page.can_edit()
if not page_edit: return
# ---
if page.isRedirect() :  return
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
save_page   = page.save(newtext='', summary='', nocreate=1, minor='')
create      = page.Create(text='', summary='')
# ---
back_links  = page.page_backlinks()
text_html   = page.get_text_html()
hidden_categories= page.get_hidden_categories()
flagged     = page.is_flagged()
timestamp   = page.get_timestamp()
user        = page.get_user()
purge       = page.purge()
'''


from newapi.ncc_page import NEW_API
# api_new  = NEW_API('www', family='nccommons')
# login    = api_new.Login_to_wiki()
# json1    = api_new.post_params(params, addtoken=False)
# pages    = api_new.Find_pages_exists_or_not(liste)
# pages    = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)
# search   = api_new.Search(value='', ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
# newpages = api_new.Get_Newpages(limit="max", namespace="0", rcstart="", user='')
# usercont = api_new.UserContribs(user, limit=5000, namespace="*", ucshow="")
# l_links  = api_new.Get_langlinks_for_list(titles, targtsitecode="", numbes=50)
# text_w   = api_new.expandtemplates(text)
# subst    = api_new.Parse_Text('{{subst:page_name}}', title)
# revisions= api_new.get_revisions(title)

"""

# ---
import configparser
from pathlib import Path

# ---
from newapi.super import super_login
from newapi.super import bot_api
from newapi.super import super_page
from newapi.super import catdepth_new

# ---

catdepth_new.SITECODE = "www"
catdepth_new.FAMILY = "nccommons"

Dir = str(Path(__file__).parents[0])
# ---
dir2 = Dir.replace('\\', '/')
dir2 = dir2.split('/pybot/')[0]
# ---
if dir2.startswith('I:'):
    dir2 = 'I:/mdwiki'
# ---
config = configparser.ConfigParser()
config.read(f"{dir2}/confs/nccommons_user.ini")
# ---
print(f"{dir2}/confs/nccommons_user.ini")
# ---
print(list(config["DEFAULT"].keys()))
# ---
username = config["DEFAULT"]["username"].strip()
password = config["DEFAULT"]["password"].strip()
# ---
User_tables = {
    "username": username,
    "password": password
}
# ---
super_login.User_tables['nccommons'] = User_tables
# ---
Login = super_login.Login
# ---
bot_api.login_def = Login
super_page.login_def = Login
catdepth_new.login_def = Login
# ---
NEW_API = bot_api.NEW_API
MainPage = super_page.MainPage
change_codes = super_page.change_codes
CatDepth = catdepth_new.subcatquery
CatDepthLogin = catdepth_new.login_wiki
# ---
# xxxxxxxxxxx


def test():
    '''
    page      = MainPage(title, 'www', family='nccommons')
    exists    = page.exists()
    text      = page.get_text()
    timestamp = page.get_timestamp()
    user      = page.get_user()
    links     = page.page_links()
    words     = page.get_words()
    purge     = page.purge()
    templates = page.get_templates()
    save_page = page.save(newtext='', summary='', nocreate=1, minor='')
    create    = page.Create(text='', summary='')
    '''
    # ---
    page = MainPage("Bilateral mesial temporal polymicrogyria (Radiopaedia 76456-88181 Axial SWI)", 'www', family='nccommons')
    # ---
    text = page.get_text()
    print(text)

    # ---
    print('---------------------------')
    cat_members = CatDepth('Category:Atlasdermatologico', sitecode='www', family="nccommons", ns="all")
    print('cat_members:')
    print(len(cat_members))
    # ---
    # sort cat_members
    cat_members = dict(sorted(cat_members.items()))
    # ---
    for x in cat_members:
        if not x.startswith('File:'):
            print(x)
    # ---
    # ex = page.page_backlinks()
    # print('---------------------------')
    # print(f'page_backlinks:{ex}')
    # ---
    # hidden_categories= page.get_hidden_categories()
    # print('---------------------------')
    # print(f'hidden_categories:{hidden_categories}')
    # ---
    # red = page.page_links()
    # print(f'page_links:{red}')
    # ---
    # save = page.save(newtext='')


# ---
if __name__ == '__main__':
    # python3 core8/pwb.py newapi/ncc_page
    super_page.print_test[1] = True
    super_login.print_test[1] = True
    test()
# ---
