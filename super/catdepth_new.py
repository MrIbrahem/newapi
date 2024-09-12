"""

from newapi.ncc_page import CatDepth, CatDepthLogin
# CatDepthLogin(sitecode="www", family="nccommons")
# cat_members = CatDepth(title, sitecode='www', family="nccommons", depth=0, ns=10, nslist=[], onlyns=False, tempyes=[])

"""
import time
import sys
import tqdm
from newapi import printe
from newapi.super.botapi_bots.bot import BOTS_APIS
from newapi.super.super_login import Login

SITECODE = "en"
FAMILY = "wikipedia"

User_tables = {}

ns_list = {
    "0": "",
    "1": "نقاش",
    "2": "مستخدم",
    "3": "نقاش المستخدم",
    "4": "ويكيبيديا",
    "5": "نقاش ويكيبيديا",
    "6": "ملف",
    "7": "نقاش الملف",
    "10": "قالب",
    "11": "نقاش القالب",
    "12": "مساعدة",
    "13": "نقاش المساعدة",
    "14": "تصنيف",
    "15": "نقاش التصنيف",
    "100": "بوابة",
    "101": "نقاش البوابة",
    "828": "وحدة",
    "829": "نقاش الوحدة",
}


# class CategoryDepth(Login):
class CategoryDepth(Login, BOTS_APIS):
    def __init__(self, title, sitecode=SITECODE, family=FAMILY, depth=0, ns="all", nslist=[], onlyns=False, without_lang="", with_lang="", tempyes=[], no_gcmsort=False, props=None, only_titles=False, printtest=False, **kwargs):
        # ---
        super().__init__(sitecode, family)
        # ---
        props = [props] if isinstance(props, str) else props
        # ---
        self.print_s = kwargs.get("print_s", True)
        self.gcmlimit = kwargs.get("gcmlimit") or 1000
        self.no_props = kwargs.get("no_props") or False
        # ---
        self.printtest = printtest
        self.props = props or []
        self.title = title
        self.no_gcmsort = no_gcmsort
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
        self.revids = {}
        self.timestamps = {}
        self.result_table = {}

        if User_tables != {}:
            for f, tab in User_tables.items():
                self.add_User_tables(f, tab)

    def Login_to_wiki(self):
        self.log_to_wiki_1()
        return

    def params_work(self, params):
        """Process parameters for a specific operation.

        This method modifies the input parameters based on various conditions
        related to the object's attributes. It adjusts properties, language
        links, and types based on the current state of the object and the
        provided parameters. The method ensures that only relevant properties
        are included in the final parameters dictionary, which is then returned
        for further processing.

        Args:
            params (dict): A dictionary of parameters to be processed.

        Returns:
            dict: The modified parameters dictionary after processing.
        """

        t_props = ["revisions"] if not self.no_gcmsort else []
        # ---
        if self.no_props:
            t_props = []
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
        if not self.no_props:
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
                params["rvprop"] = "timestamp|ids"
        # ---
        return params

    def pages_table_work(self, table, pages):
        """Update the pages table with information from the provided pages.

        This method processes a dictionary of pages, extracting relevant
        information such as timestamps, revision IDs, namespaces, templates,
        language links, and categories. It updates the provided table with this
        information, ensuring that it maintains a structured format.

        Args:
            table (dict): A dictionary representing the current state of the
                pages table to be updated.
            pages (dict): A dictionary containing page information, where each
                key is a category and each value is a dictionary with details
                about that category.

        Returns:
            dict: The updated pages table after processing the input pages.
        """

        # ---
        for category in pages:
            caca = pages[category] if isinstance(pages, dict) else category
            cate_title = caca["title"]
            # ---
            timestamp = caca.get("revisions", [{}])[0].get("timestamp", "")
            self.timestamps[cate_title] = timestamp
            # ---
            revid = caca.get("revisions", [{}])[0].get("revid", "")
            self.revids[cate_title] = revid
            # ---
            p_ns = str(caca.get("ns", 0))
            # ---
            tablese = table.get(cate_title, {})
            if revid:
                tablese["revid"] = revid
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
        params = {
            "action": "query",
            "format": "json",
            "utf8": 1,
            "generator": "categorymembers",
            "gcmprop": "title",
            # "prop": "revisions",
            "gcmtype": "page|subcat",
            "gcmlimit": self.gcmlimit,
            "formatversion": "1",
            "gcmsort": "timestamp",
            "gcmdir": "newer",
            # "rvprop": "timestamp",
        }
        # ---
        params = self.params_work(params)
        # ---
        params["gcmtitle"] = cac
        params["action"] = "query"
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
        if self.print_s:
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
    print_s = kwargs.get("print_s", True)
    # ---
    priffixs = {"ar": "تصنيف:", "en": "Category:"}
    # ---
    start_priffix = priffixs.get(sitecode)
    # ---
    if start_priffix and not title.startswith(start_priffix):
        title = start_priffix + title
    # ---
    if print_s:
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
    if print_s:
        printe.output(f"<<lightblue>>catdepth_new.py: find {len(result)} pages({ns}) in {sitecode}:{title}, depth:{depth} in {delta} seconds")
    # ---
    return result


def login_wiki(sitecode=SITECODE, family=FAMILY):
    # ---
    bot = CategoryDepth("", sitecode=sitecode, family=family)
    # ---
    bot.log_to_wiki_1()
