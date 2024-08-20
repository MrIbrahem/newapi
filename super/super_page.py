"""
Usage:
# ---
from newapi.mdwiki_page import MainPage
page      = MainPage(title, 'www', family='mdwiki')
# ---
from newapi.page import MainPage
page      = MainPage(title, 'ar', family='wikipedia')
# ---
'''
if not page.exists(): return
# ---
page_edit = page.can_edit(script='fixref|cat|stub|tempcat|portal')
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
'''

"""
import os
import pywikibot
from warnings import warn
import sys
import wikitextparser as wtp
from newapi import printe
from newapi import txtlib
from newapi import botEdit

from newapi.super.page_bots.ar_err import find_edit_error
from newapi.super.page_bots.bot import APIS
from newapi.super.super_login import Login
from newapi.except_err import exception_err, warn_err

file_name = os.path.basename(__file__)

print_test = {1: False}
# ---
Edit_summary_line = {1: " -Edit summary: %s:"}
# ---
User_tables = {}
# ---
not_loged_m = {1: ""}
Save_Edit_Pages = {1: False}
# ---
change_codes = {
    "nb": "no",
    "bat_smg": "bat-smg",
    "be_x_old": "be-tarask",
    "be-x-old": "be-tarask",
    "cbk_zam": "cbk-zam",
    "fiu_vro": "fiu-vro",
    "map_bms": "map-bms",
    "nds_nl": "nds-nl",
    "roa_rup": "roa-rup",
    "zh_classical": "zh-classical",
    "zh_min_nan": "zh-min-nan",
    "zh_yue": "zh-yue",
}


def default_user_agent():
    tool = os.getenv("HOME")
    # "/data/project/mdwiki"
    tool = tool.split("/")[-1] if tool else "himo"
    # ---
    li = f"{tool} bot/1.0 (https://{tool}.toolforge.org/; tools.{tool}@toolforge.org)"
    # ---
    # printe.output(f"default_user_agent: {li}")
    # ---
    return li

class MainPage(Login, APIS):
    def __init__(self, title, lang, family="wikipedia"):
        # print(f"class MainPage: {lang=}")
        # ---
        self.username = ""
        # ---
        super().__init__(lang, family)
        # ---
        self.title = title
        # ---
        self.lang = change_codes.get(lang) or lang
        # ---
        self.family = family
        self.endpoint = f"https://{lang}.{family}.org/w/api.php"
        # ---
        self.userinfo = {}
        self.Exists = ""
        self.is_redirect = ""
        self.is_Disambig = False
        self.flagged = ""
        self.can_be_edit = False
        # ---
        self.wikibase_item = ""
        self.text = ""
        self.text_html = ""
        # ---
        self.revid = ""
        self.newrevid = ""
        # ---
        self.pageid = ""
        self.timestamp = ""
        self.user = ""
        # ---
        self.revisions = []
        self.back_links = []
        self.extlinks = []
        self.links = []
        self.iwlinks = []
        self.links_here = []
        # ---
        self.info = {"done": False}
        # ---
        self.categories = {}
        self.hidden_categories = {}
        self.all_categories_with_hidden = {}
        # ---
        self.langlinks = {}
        self.templates = {}
        self.templates_API = {}

        self.summary = ""
        self.words = 0
        self.length = 0
        self.ns = False
        self.newtext = ""
        # ---
        if User_tables != {}:
            for f, tab in User_tables.items():
                self.add_User_tables(f, tab)
        # ---
        if self.lang not in ["", not_loged_m[1]]:
            # ---
            self.Log_to_wiki()
            # ---
            not_loged_m[1] = self.lang

    def ask_put(self, nodiff=False, ASK=False):
        yes_answer = ["y", "a", "", "Y", "A", "all", "aaa"]
        # ---
        if "ask" in sys.argv and not Save_Edit_Pages[1] or print_test[1] or ASK:
            # ---
            if "nodiff" not in sys.argv and not nodiff:
                if len(self.newtext) < 70000 and len(self.text) < 70000 or "diff" in sys.argv:
                    printe.showDiff(self.text, self.newtext)
                else:
                    printe.output("showDiff error..")
            # ---
            printe.output(f"diference in bytes: {len(self.newtext) - len(self.text):,}")
            printe.output(f"len of text: {len(self.text):,}, len of newtext: {len(self.newtext):,}")
            # ---
            printe.output(Edit_summary_line[1] % self.summary)
            # ---
            sa = pywikibot.input(f"<<lightyellow>>page.py: Do you want to accept these changes? (yes, no): for page {self.lang}:{self.title}? {self.username=}")
            # ---
            if sa == "a":
                printe.output("<<lightgreen>> ---------------------------------")
                printe.output(f"<<lightgreen>> {file_name} save all without asking.")
                printe.output("<<lightgreen>> ---------------------------------")
                Save_Edit_Pages[1] = True
            # ---
            if sa not in yes_answer:
                printe.output("wrong answer")
                return False
        # ---
        return True

    def false_edit(self):
        # self.newtext
        # self.text
        # ---
        if self.ns != 0 or "nofa" in sys.argv:
            return False
        # ---
        if not self.text:
            self.text = self.get_text()
        # ---
        # If the new edit will remove 90% of the text, return False
        if len(self.newtext) < 0.1 * len(self.text):
            text_err = f"Edit will remove 90% of the text. {len(self.newtext)} < 0.1 * {len(self.text)}"
            text_err += f"title: {self.title}, summary: {self.summary}"
            exception_err("", text=text_err)
            return True
        # ---
        if self.lang == "ar" and self.ns == 0:
            if find_edit_error(self.text, self.newtext):
                return True
        # ---
        return False

    def import_page(self, family="wikipedia"):
        params = {
            "action": "import",
            "format": "json",
            "interwikisource": family,
            "interwikipage": self.title,
            "fullhistory": 1,
            "assignknownusers": 1,
        }
        # ---
        data = self.post_params(params)
        # ---
        done = data.get("import", [{}])[0].get("revisions", 0)
        # ---
        printe.output(f"<<lightgreen>> imported {done} revisions")
        # ---
        return data

    def get_text(self, redirects=False):
        params = {
            "action": "query",
            "prop": "revisions|pageprops|flagged",
            "titles": self.title,
            "ppprop": "wikibase_item",
            "rvprop": "timestamp|content|user|ids",
            "rvslots": "*",
        }  # pageprops  # revisions  # revisions
        # ---
        if redirects:
            params["redirects"] = 1
        data = self.post_params(params)
        # ---
        # _dat_ = { "batchcomplete": "", "query": { "normalized": [{ "from": "وب:ملعب", "to": "ويكيبيديا:ملعب" }], "pages": { "361534": { "pageid": 361534, "ns": 4, "title": "ويكيبيديا:ملعب", "revisions": [{ "revid": 61421668, "parentid": 61421528, "user": "Al-shazali Sabeel", "timestamp": "2023-03-07T13:50:29Z", "slots": { "main": { "contentmodel": "wikitext", "contentformat": "text/x-wiki", "*": "{{عنوان الملعب}}" } } }], "pageprops": { "wikibase_item": "Q3938" } } } }, }
        # ---
        pages = data.get("query", {}).get("pages", {})
        # ---
        for k, v in pages.items():
            # ---
            if print_test[1] or "printdata" in sys.argv:
                warn(warn_err(f"v:{str(v)}"), UserWarning)
            # ---
            if "missing" in v or k == "-1":
                self.Exists = False
                break
            else:
                self.Exists = True
            # ---
            # title = v["title"]
            # ---
            pageprops = v.get("pageprops", {})
            self.wikibase_item = pageprops.get("wikibase_item") or self.wikibase_item
            # ---
            # "flagged": { "stable_revid": 61366100, "level": 0, "level_text": "stable"}
            self.flagged = v.get("flagged", False) is not False
            # ---
            self.ns = v.get("ns") or self.ns
            self.pageid = v.get("pageid") or self.pageid
            # ---
            page = v.get("revisions", [{}])[0]
            # ---
            self.text = page.get("slots", {}).get("main", {}).get("*", "")
            self.user = page.get("user") or self.user
            self.revid = page.get("revid") or self.revid
            # ---
            self.timestamp = page.get("timestamp") or self.timestamp
            # ---
            break
        # ---
        return self.text

    def get_infos(self):
        # ---
        params = {
            "action": "query",
            "titles": self.title,
            "prop": "categories|langlinks|templates|linkshere|iwlinks|info",
            "clprop": "sortkey|hidden",
            "cllimit": "max",  # categories
            "lllimit": "max",  # langlinks
            "tllimit": "max",  # templates
            "lhlimit": "max",  # linkshere
            "iwlimit": "max",  # iwlinks
            "formatversion": "2",
            # "normalize": 1,
            "tlnamespace": "10",
        }
        # ---
        # _data_ = { "continue": {}, "query": { "pages": { "9124097": { "pageid": 9124097, "ns": 0, "title": "طواف العالم للدراجات 2023", "categories": [], "langlinks": [], "templates": [{ "ns": 10, "title": "قالب:-" }], "linkshere": [{ "pageid": 189150, "ns": 0, "title": "طواف فرنسا" }], "iwlinks": [{ "prefix": "commons", "*": "Category:2023_UCI_World_Tour" }], "contentmodel": "wikitext", "pagelanguage": "ar", "pagelanguagehtmlcode": "ar", "pagelanguagedir": "rtl", "touched": "2023-03-07T11:53:53Z", "lastrevid": 61366100, "length": 985, } } }, }
        # ---
        data = self.post_params(params)
        # ---
        # xs = { 'batchcomplete': True, 'query': { 'pages': [{ 'pageid': 151314, 'ns': 10, 'title': 'قالب:أوب', 'categories': [{ 'ns': 14, 'title': 'تصنيف:قوالب تستخدم أنماط القوالب', 'sortkey': '', 'sortkeyprefix': '', 'hidden': False }, { 'ns': 14, 'title': 'تصنيف:cc', 'sortkey': 'v', 'sortkeyprefix': 'أوب', 'hidden': True }], 'langlinks': [{ 'lang': 'bh', 'title': 'टेम्पलेट:AWB' }], 'templates': [{ 'ns': 10, 'title': 'قالب:No redirect' }], 'linkshere': [{ 'pageid': 308641, 'ns': 10, 'title': 'قالب:AWB', 'redirect': True }], 'iwlinks': [{ 'prefix': 'd', 'title': 'Q4063270' }], 'contentmodel': 'wikitext', 'pagelanguage': 'ar', 'pagelanguagehtmlcode': 'ar', 'pagelanguagedir': 'rtl', 'touched': '2023-03-05T22:10:23Z', 'lastrevid': 61388266, 'length': 3477, }] }, }
        # ---
        ta = data.get("query", {}).get("pages", [{}])[0]
        # ---
        # for _, ta in pages.items():
        # ---
        self.ns = ta.get("ns") or self.ns
        self.pageid = ta.get("pageid") or self.pageid
        self.length = ta.get("length") or self.length
        self.revid = ta.get("lastrevid") or self.revid
        # ---
        self.is_redirect = True if "redirect" in ta else False
        # ---
        for cat in ta.get("categories", []):
            # ---
            # _cat_ = { "ns": 14, "title": "تصنيف:بوابة سباق الدراجات الهوائية/مقالات متعلقة", "sortkey": "d8b7", "sortkeyprefix": "", "hidden": True }
            # ---
            if "sortkey" in cat:
                del cat["sortkey"]
            # ---
            tit = cat["title"]
            # ---
            self.all_categories_with_hidden[tit] = cat
            # ---
            if cat.get("hidden") is True:
                self.hidden_categories[tit] = cat
            else:
                del cat["hidden"]
                self.categories[tit] = cat
        # ---
        if ta.get("langlinks", []) != []:
            # ---
            # {"lang": "ca", "*": "UCI World Tour 2023"} or {'lang': 'bh', 'title': 'टेम्पलेट:AWB'}
            # ---
            self.langlinks = {ta["lang"]: ta.get("*") or ta.get("title") for ta in ta.get("langlinks", [])}
        # ---
        if ta.get("templates", []) != []:
            # ---
            # 'templates': [{'ns': 10, 'title': 'قالب:No redirect'}],
            # ---
            self.templates_API = [ta["title"] for ta in ta.get("templates", [])]
        # ---
        # "linkshere": [{"pageid": 189150,"ns": 0,"title": "طواف فرنسا"}, {"pageid": 308641,"ns": 10,"title": "قالب:AWB","redirect": ""}]
        self.links_here = ta.get("linkshere", [])
        # ---
        self.iwlinks = ta.get("iwlinks", [])
        # ---
        self.info["done"] = True

    def get_text_html(self):
        params = {
            "action": "parse",
            "page": self.title,
            "formatversion": "2",
            "prop": "text",
        }
        # ---
        data = self.post_params(params)
        # ---
        # _data_ = { 'warnings': { 'main': { 'warnings': 'Unrecognized parameter: bot.' } }, 'parse': { 'title': 'ويكيبيديا:ملعب', 'pageid': 361534, 'text': '' } }
        # ---
        self.text_html = data.get("parse", {}).get("text", "")
        # ---
        return self.text_html

    def get_redirect_target(self):
        # ---
        params = {
            "action": "query",
            "titles": self.title,
            "prop": "info",
            "redirects": 1,
        }
        # ---
        data = self.post_params(params)
        # ---
        # _pages_ = { 'batchcomplete': '', 'query': { 'redirects': [{ 'from': 'Yemen', 'to': 'اليمن' }], 'pages': {}, 'normalized': [{ 'from': 'yemen', 'to': 'Yemen' }] } }
        # ---
        _redirects = {"from": "Yemen", "to": "اليمن"}
        # ---
        redirects = data.get("query", {}).get("redirects", [{}])[0]
        # ---
        to = redirects.get("to", "")
        # ---
        if to:
            printe.output(f"<<lightyellow>>Page:{self.title} redirect to {to}")
        # ---
        return to

    def get_words(self):
        srlimit = "30"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": self.title,
            "srlimit": srlimit,
        }
        data = self.post_params(params, addtoken=True)
        # ---
        if not data:
            return 0
        # ---
        search = data.get("query", {}).get("search", [])
        # ---
        for pag in search:
            tit = pag["title"]
            if tit == self.title:
                count = pag["wordcount"]
                self.words = count
                break
        # ---
        return self.words

    def get_extlinks(self):
        params = {
            "action": "query",
            "format": "json",
            "prop": "extlinks",
            "titles": self.title,
            "formatversion": "2",
            "utf8": 1,
            "ellimit": "max",
        }
        # ---
        links = []
        # ---
        continue_params = {}
        # ---
        d = 0
        # ---
        while continue_params != {} or d == 0:
            # ---
            d += 1
            # ---
            if continue_params:
                # params = {**params, **continue_params}
                params.update(continue_params)
            # ---
            json1 = self.post_params(params)
            # ---
            continue_params = json1.get("continue", {})
            # ---
            linkso = json1.get("query", {}).get("pages", [{}])[0].get("extlinks", [])
            # ---
            links.extend(linkso)
        # ---
        links = [x["url"] for x in links]
        # ---
        # remove duplicates
        liste1 = sorted(set(links))
        # ---
        self.extlinks = liste1
        return liste1

    def get_userinfo(self):
        if len(self.userinfo) == 0:
            params = {
                "action": "query",
                "format": "json",
                "list": "users",
                "formatversion": "2",
                "usprop": "groups",
                "ususers": self.user,
            }
            # ---
            data = self.post_params(params)
            # ---
            # _userinfo_ = { "id": 229481, "name": "Mr. Ibrahem", "groups": ["editor", "reviewer", "rollbacker", "*", "user", "autoconfirmed"] }
            # ---
            ff = data.get("query", {}).get("users", [{}])
            # ---
            if ff:
                self.userinfo = ff[0]
        # ---
        return self.userinfo

    def isRedirect(self):
        # ---
        if not self.is_redirect:
            self.get_infos()
        # ---
        return self.is_redirect

    def isDisambiguation(self):
        # ---
        # if the title ends with '(توضيح)' or '(disambiguation)'
        self.is_Disambig = self.title.endswith("(توضيح)") or self.title.endswith("(disambiguation)")
        # ---
        if self.is_Disambig:
            printe.output(f'<<lightred>> page "{self.title}" is Disambiguation / توضيح')
        # ---
        return self.is_Disambig

    def get_categories(self, with_hidden=False):
        # ---
        # if not self.categories: self.get_infos()
        if not self.info["done"]:
            self.get_infos()
        # ---
        if with_hidden:
            return self.all_categories_with_hidden
        # ---
        return self.categories

    def get_hidden_categories(self):
        # ---
        if self.categories == {} and self.hidden_categories == {}:
            self.get_infos()
        # ---
        return self.hidden_categories

    def get_langlinks(self):
        # ---
        if not self.info["done"]:
            self.get_infos()
        # ---
        return self.langlinks

    def get_templates_API(self):
        # ---
        if not self.info["done"]:
            self.get_infos()
        # ---
        return self.templates_API

    def get_links_here(self):
        # ---
        if not self.info["done"]:
            self.get_infos()
        # ---
        return self.links_here

    def get_wiki_links_from_text(self):
        if not self.text:
            self.text = self.get_text()
        # ---
        parsed = wtp.parse(self.text)
        wikilinks = parsed.wikilinks
        # ---
        # printe.output(f'wikilinks:{str(wikilinks)}')
        # ---
        # for x in wikilinks:
        #     print(x.title)
        # ---
        return wikilinks

    def Get_tags(self, tag=""):
        if not self.text:
            self.text = self.get_text()
        # ---
        self.text = self.text.replace("<ref>", '<ref name="ss">', 1)
        # ---
        parsed = wtp.parse(self.text)
        tags = parsed.get_tags()
        # ---
        # printe.output(f'tags:{str(tags)}')
        # ---
        if not tag:
            return tags
        # ---
        new_tags = []
        # ---
        for x in tags:
            if x.name == tag:
                new_tags.append(x)
        # ---
        # return tags if tag == '' else [x for x in tags if x.name == tag]
        # ---
        return new_tags

    def can_edit(self, script=""):
        # ---
        if self.family != "wikipedia":
            return True
        # ---
        if not self.text:
            self.text = self.get_text()
        # ---
        self.can_be_edit = botEdit.bot_May_Edit(text=self.text, title_page=self.title, botjob=script)
        # ---
        return self.can_be_edit

    def is_flagged(self):
        # ---
        if not self.text:
            self.text = self.get_text()
        # ---
        return self.flagged

    def get_timestamp(self):
        if not self.timestamp:
            self.get_text()
        return self.timestamp

    def exists(self):
        if not self.Exists:
            self.get_text()
        if not self.Exists:
            printe.output(f'page "{self.title}" not exists in {self.lang}:{self.family}')
        return self.Exists

    def namespace(self):
        if self.ns is False:
            self.get_text()
        return self.ns

    def get_user(self):
        if not self.user:
            self.get_text()
        return self.user

    def get_templates(self):
        if not self.text:
            self.text = self.get_text()
        self.templates = txtlib.extract_templates_and_params(self.text)
        return self.templates

    def save(self, newtext="", summary="", nocreate=1, minor="", tags="", nodiff=False, ASK=False):
        # ---
        self.newtext = newtext
        if summary:
            self.summary = summary
        # ---
        if self.false_edit():
            return False
        # ---
        ask = self.ask_put(nodiff=nodiff, ASK=ASK)
        if ask is False:
            return False
        # ---
        params = {
            "action": "edit",
            "title": self.title,
            "text": newtext,
            "summary": self.summary,
            "minor": minor,
            "nocreate": nocreate,
        }
        # ---
        if nocreate != 1:
            del params["nocreate"]
        # ---
        if self.revid:
            params["baserevid"] = self.revid
        # ---
        if tags:
            params["tags"] = tags
        # ---
        # params['basetimestamp'] = self.timestamp
        # ---
        pop = self.post_params(params, addtoken=True)
        # ---
        if not pop:
            return False
        # ---
        error = pop.get("error", {})
        edit = pop.get("edit", {})
        result = edit.get("result", "")
        # ---
        # {'edit': {'result': 'Success', 'pageid': 5013, 'title': 'User:Mr. Ibrahem/sandbox', 'contentmodel': 'wikitext', 'oldrevid': 1336986, 'newrevid': 1343447, 'newtimestamp': '2023-04-01T23:14:07Z', 'watched': ''}}
        # ---
        if result.lower() == "success":
            self.text = newtext
            self.user = ""
            printe.output(f"<<lightgreen>> ** true .. [[{self.lang}:{self.family}:{self.title}]] ")
            # printe.output('Done True...')
            # ---
            if "printpop" in sys.argv:
                print(pop)
            # ---
            self.pageid = edit.get("pageid") or self.pageid
            self.revid = edit.get("newrevid") or self.revid
            self.newrevid = edit.get("newrevid") or self.newrevid
            self.timestamp = edit.get("newtimestamp") or self.timestamp
            # ---
            return True
        # ---
        if error != {}:
            print(pop)
            er = self.handel_err(error, function="Save",  params=params)
            # ---
            return er
        # ---
        return False

    def purge(self):
        # ---
        params = {
            "action": "purge",
            "forcelinkupdate": 1,
            "forcerecursivelinkupdate": 1,
            "titles": self.title,
        }
        # ---
        data = self.post_params(params, addtoken=True)
        # ---
        if not data:
            printe.output("<<lightred>> ** purge error. ")
            return False
        # ---
        title2 = self.title
        # ---
        #  'normalized': [{'from': 'وب:ملعب', 'to': 'ويكيبيديا:ملعب'}]}
        # ---
        for x in data.get("normalized", []):
            # printe.output(f"normalized from {x['from']} to {x['to']}")
            if x["from"] == self.title:
                title2 = x["to"]
                break
        # ---
        for t in data.get("purge", []):
            # t = [{'ns': 4, 'title': 'ويكيبيديا:ملعب', 'purged': '', 'linkupdate': ''}]
            ti = t["title"]
            if title2 == ti and "purged" in t:
                return True
            if "missing" in t:
                printe.output(f"page \"{t['title']}\" missing")
                return "missing"
        return False

    def Create(self, text="", summary=""):
        # ---
        self.newtext = text
        # ---
        ask = self.ask_put()
        # ---
        if ask is False:
            return False
        # ---
        params = {
            "action": "edit",
            "title": self.title,
            "text": text,
            "summary": summary,
            "notminor": 1,
            "createonly": 1,
        }
        # ---
        pop = self.post_params(params, addtoken=True)
        # ---
        if not pop:
            return False
        # ---
        error = pop.get("error", {})
        edit = pop.get("edit", {})
        result = edit.get("result", "")
        # ---
        if print_test[1]:
            print("pop:")
            print(pop)
        # ---
        if result.lower() == "success":
            # ---
            # {'edit': {'new': '', 'result': 'Success', 'pageid': 9090918, 'title': 'مستخدم:Mr. Ibrahem/test2024', 'contentmodel': 'wikitext', 'oldrevid': 0, 'newrevid': 61016221, 'newtimestamp': '2023-02-01T21:52:42Z'}}
            # ---
            self.text = text
            # ---
            printe.output(f"<<lightgreen>> ** true .. [[{self.lang}:{self.family}:{self.title}]] ")
            # printe.output('Done True... time.sleep() ')
            # ---
            self.pageid = edit.get("pageid") or self.pageid
            self.revid = edit.get("newrevid") or self.revid
            self.newrevid = edit.get("newrevid") or self.newrevid
            self.timestamp = edit.get("newtimestamp") or self.timestamp
            # ---
            return True
        # ---
        if error != {}:
            print(pop)
            er = self.handel_err(error, function="Create", params=params)
            # ---
            return er
            # ---
        return False
