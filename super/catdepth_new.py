"""

from newapi.ncc_page import CatDepth, CatDepthLogin
# CatDepthLogin(sitecode="www", family="nccommons")
# cat_members = CatDepth(title, sitecode='www', family="nccommons", depth=0, ns=10, nslist=[], onlyns=False, tempyes=[])

"""
import time
import sys
import tqdm
from newapi import printe

SITECODE = "en"
FAMILY = "wikipedia"


def login_def(lang, family):
    return {}


ns_list = {"0": "", "1": "نقاش", "2": "مستخدم", "3": "نقاش المستخدم", "4": "ويكيبيديا", "5": "نقاش ويكيبيديا", "6": "ملف", "7": "نقاش الملف", "10": "قالب", "11": "نقاش القالب", "12": "مساعدة", "13": "نقاش المساعدة", "14": "تصنيف", "15": "نقاش التصنيف", "100": "بوابة", "101": "نقاش البوابة", "828": "وحدة", "829": "نقاش الوحدة"}


class CategoryDepth:
    def __init__(self, title, sitecode=SITECODE, family=FAMILY, depth=0, ns="all", nslist=[], onlyns=False, without_lang="", with_lang="", tempyes=[], no_gcmsort=False, props=None, only_titles=False, **kwargs):
        # ---
        props = [props] if isinstance(props, str) else props
        # ---
        self.props = props or []
        self.title = title
        self.no_gcmsort = no_gcmsort
        # ---
        self.log = login_def(sitecode, family=family)
        # ---
        self.only_titles = only_titles
        self.onlyns = onlyns
        self.tempyes = tempyes

        self.without_lang = without_lang
        self.with_lang = with_lang

        self.depth = depth
        self.ns = str(ns)
        self.nslist = nslist
        if not isinstance(self.depth, int):
            try:
                self.depth = int(self.depth)
            except ValueError:
                print(f"self.depth != int: {self.depth}")
                self.depth = 0
        # ---
        self.timestamps = {}
        self.result_table = {}
        self.params = {}
        self.make_params()

        # return self.subcatquery_(title)

    def Login_to_wiki(self):
        self.log.Log_to_wiki()

    def post_params(self, params):
        return self.log.post(params, addtoken=True)

    def make_params(self):
        t_props = ["revisions"] if not self.no_gcmsort else []
        # ---
        params = {
            "action": "query",
            "format": "json",
            "utf8": 1,
            "generator": "categorymembers",
            "gcmprop": "title",
            # "prop": "revisions",
            "gcmtype": "page|subcat",
            "gcmlimit": "1000",
            "formatversion": "1",
            "gcmsort": "timestamp",
            "gcmdir": "newer",
            # "rvprop": "timestamp",
        }
        # ---
        if self.no_gcmsort:
            del params["gcmsort"]
            del params["gcmdir"]
        # ---
        if self.tempyes != []:
            t_props.append("templates")
            params["tllimit"] = "max"
            params["tltemplates"] = "|".join(self.tempyes)
        # ---
        if self.with_lang or self.without_lang:  # مع وصلة لغة معينة
            t_props.append("langlinks")
            params["lllimit"] = "max"
        # ---
        if self.ns in ["0", "10"]:
            params["gcmtype"] = "page"
        elif self.ns in [14]:
            params["gcmtype"] = "subcat"
        # ---
        # print('gcmtype::', params["gcmtype"])
        # ---
        if len(self.nslist) > 0:
            if self.nslist == [14]:
                params["gcmtype"] = "subcat"
            elif 14 not in self.nslist and self.depth == 0:
                params["gcmtype"] = "page"
        # ---
        # print('gcmtype::', params["gcmtype"])
        # ---
        for x in self.props:
            if x not in t_props:
                t_props.append(x)
        # ---
        if len(t_props) > 0:
            params["prop"] = "|".join(t_props)
        # ---
        if "categories" in params["prop"]:
            # params["clprop"] = "hidden"
            params["cllimit"] = "max"
        # ---
        if "revisions" in params["prop"]:
            params["rvprop"] = "timestamp"
        # ---
        self.params = params

    def pages_table_work(self, table, pages):
        # ---
        for category in pages:
            caca = pages[category] if isinstance(pages, dict) else category
            cate_title = caca["title"]
            # ---
            timestamp = caca.get("revisions", [{}])[0].get("timestamp", "")
            self.timestamps[cate_title] = timestamp
            # ---
            p_ns = str(caca.get("ns", 0))
            # ---
            tablese = table.get(cate_title, {})
            # ---
            if p_ns:
                tablese["ns"] = caca["ns"]
                # ---
                if self.ns == "14" or self.nslist == [14]:
                    if p_ns != "14":
                        continue
                # ---
                if self.ns == "0" or self.nslist == [0]:
                    if p_ns != "0":
                        continue
                # ---
                # do same for ns_list
                # if self.ns in ns_list:
                #     if p_ns not in ns_list:
                #         continue
            # ---
            templates = [x["title"] for x in caca.get("templates", {})]
            # ---
            if templates:
                if tablese.get("templates"):
                    tablese["templates"].extend(templates)
                else:
                    tablese["templates"] = templates
                # ---
                tablese["templates"] = list(set(tablese["templates"]))
            # ---
            langlinks = {fo["lang"]: fo.get("title") or fo.get("*") or "" for fo in caca.get("langlinks", [])}
            # ---
            if langlinks:
                if tablese.get("langlinks"):
                    tablese["langlinks"].update(langlinks)
                else:
                    tablese["langlinks"] = langlinks
            # ---
            # categories = {x["title"]: x for x in caca.get("categories", {})}
            categories = [x["title"] for x in caca.get("categories", {})]
            # ---
            if categories:
                if tablese.get("categories"):
                    tablese["categories"].extend(categories)
                else:
                    tablese["categories"] = categories
            # ---
            table[cate_title] = tablese
        # ---
        return table

    def get_cat_new(self, cac):
        # ---
        # print("get_cat_new")
        # ---
        params = self.params
        params["gcmtitle"] = cac
        # ---
        results = {}
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
            api_data = self.post_params(params)
            # ---
            if not api_data:
                print(f"api is False for {cac}")
                break
            # ---
            continue_params = api_data.get("continue", {})
            # ---
            pages = api_data.get("query", {}).get("pages", {})
            # ---
            results = self.pages_table_work(results, pages)
        # ---
        return results

    def add_to_result_table(self, x, tab):
        if self.without_lang:
            no_langs = tab.get("langlinks", {}).get(self.without_lang, "")
            if no_langs:
                return

        if self.with_lang:
            langs = tab.get("langlinks", {}).get(self.with_lang, "")
            if not langs:
                return

        if self.onlyns:
            p_ns = str(tab.get("ns", 0))
            if p_ns != str(self.onlyns):
                return
        # ---
        if self.only_titles:
            self.result_table.setdefault(x, {})
            return
        # ---
        # print(tab)
        if x in self.result_table:
            tab2 = self.result_table[x].copy()
            tab2.update(tab)
            tab = tab2
        # ---
        self.result_table[x] = tab

    def subcatquery_(self):
        # ---
        print(f"catdepyh_new.py cat:{self.title}, ns:{self.ns}")
        # ---
        tablemember = self.get_cat_new(self.title)
        # ---
        for x, zz in tablemember.items():
            self.add_to_result_table(x, zz)
        # ---
        new_list = [x for x, xx in tablemember.items() if int(xx["ns"]) == 14]
        # ---
        depth_done = 0
        # ---
        while self.depth > depth_done:
            new_tab2 = []
            # ---
            depth_done += 1
            # ---
            # printe.output(f"<<yellow>> work in subcats: {len(new_list)}, depth:{depth_done}/{self.depth}:")
            # ---
            for cat in tqdm.tqdm(new_list):
                # ---
                table2 = self.get_cat_new(cat)
                # ---
                for x, v in table2.items():
                    # ---
                    if int(v["ns"]) == 14:
                        new_tab2.append(x)
                    # ---
                    self.add_to_result_table(x, v)
            # ---
            new_list = new_tab2
        # ---
        # sort self.result_table by timestamp
        if not self.no_gcmsort:
            soro = sorted(self.result_table.items(), key=lambda item: self.timestamps.get(item[0], 0), reverse=True)
            self.result_table = {k: v for k, v in soro}
        # ---
        return self.result_table


def subcatquery(title, sitecode=SITECODE, family=FAMILY, depth=0, ns="all", nslist=[], onlyns=False, without_lang="", with_lang="", tempyes=[], props=None, only_titles=False, **kwargs):
    # ---
    priffixs = {"ar": "تصنيف:", "en": "Category:"}
    # ---
    start_priffix = priffixs.get(sitecode)
    # ---
    if start_priffix and not title.startswith(start_priffix):
        title = start_priffix + title
    # ---
    printe.output(f"<<lightyellow>> catdepth_new.py sub cat query for {sitecode}:{title}, depth:{depth}, ns:{ns}, onlyns:{onlyns}")
    # ---
    start = time.time()
    final = time.time()
    # ---
    bot = CategoryDepth(title, sitecode=sitecode, family=family, depth=depth, ns=ns, nslist=nslist, onlyns=onlyns, without_lang=without_lang, with_lang=with_lang, tempyes=tempyes, props=props, only_titles=only_titles, **kwargs)
    # ---
    # bot.Login_to_wiki()
    # ---
    result = bot.subcatquery_()
    # ---
    final = time.time()
    delta = int(final - start)
    # ---
    if "printresult" in sys.argv:
        printe.output(result)
    # ---
    printe.output(f"<<lightblue>>catdepth_new.py: find {len(result)} pages({ns}) in {sitecode}:{title}, depth:{depth} in {delta} seconds")
    # ---
    return result


def login_wiki(sitecode=SITECODE, family=FAMILY):
    # ---
    bot = CategoryDepth("", sitecode=sitecode, family=family)
    # ---
    bot.log.log_to_wiki_1()
