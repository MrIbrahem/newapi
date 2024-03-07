import time
import sys
from newapi import printe


def login_def(lang, family):
    return {}


ns_list = {"0": "", "1": "نقاش", "2": "مستخدم", "3": "نقاش المستخدم", "4": "ويكيبيديا", "5": "نقاش ويكيبيديا", "6": "ملف", "7": "نقاش الملف", "10": "قالب", "11": "نقاش القالب", "12": "مساعدة", "13": "نقاش المساعدة", "14": "تصنيف", "15": "نقاش التصنيف", "100": "بوابة", "101": "نقاش البوابة", "828": "وحدة", "829": "نقاش الوحدة"}


class CategoryDepth:
    def __init__(self, title, sitecode="en", depth=0, family="wikipedia", ns="all", nslist=[], without_lang="", with_lang="", tempyes=[], no_gcmsort=False, **kwargs):
        # ---
        self.title = title
        self.no_gcmsort = no_gcmsort
        # ---
        self.log = login_def(sitecode, family=family)
        # ---
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
        params = {"action": "query", "format": "json", "utf8": 1, "generator": "categorymembers", "gcmprop": "title", "prop": ["revisions"], "gcmtype": "page|subcat", "gcmlimit": "max", "formatversion": "1", "gcmsort": "timestamp", "gcmdir": "newer", "rvprop": "timestamp"}
        # ---
        if self.no_gcmsort:
            del params["gcmsort"]
            del params["gcmdir"]

        if self.tempyes != []:
            params["prop"].append("templates")
            params["tllimit"] = "max"
            params["tltemplates"] = "|".join(self.tempyes)
        if self.with_lang != "" or self.without_lang != "":  # مع وصلة لغة معينة
            params["prop"].append("langlinks")
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
        if len(params["prop"]) == 0:
            del params["prop"]
        # ---
        self.params = params

    def get_cat(self, cac):
        # ---
        params = self.params
        params["gcmtitle"] = cac
        # ---
        continue_v = "x"
        continue_p = ""
        # ---
        table = {}
        # ---
        while continue_v != "":
            if continue_v != "x":
                params[continue_p] = continue_v
            # ---
            continue_v = ""
            # ---
            api = self.post_params(params)
            # ---
            if not api:
                print(f"api == false for {cac}")
                break
            # ---
            continue_d = api.get("continue", {})
            for p, v in continue_d.items():
                if p == "continue":
                    continue
                continue_v = v
                continue_p = p
            # ---
            pages = api.get("query", {}).get("pages", {})
            # ---
            for category in pages:
                caca = pages[category] if isinstance(pages, dict) else category
                cate_title = caca["title"]
                # ---
                timestamp = caca.get("revisions", [{}])[0].get("timestamp", "")
                self.timestamps[cate_title] = timestamp
                # ---
                tablese = {}
                # ---
                if "ns" in caca:
                    tablese["ns"] = caca["ns"]
                    if self.ns == "14" or self.nslist == [14]:
                        if str(caca["ns"]) != "14":
                            continue
                    if self.ns == "0" or self.nslist == [0]:
                        if str(caca["ns"]) != "0":
                            continue
                    # do same for ns_list
                    # if self.ns in ns_list:
                    #     if str(caca["ns"]) not in ns_list:
                    #         continue
                # ---
                tablese["templates"] = [x["title"] for x in caca.get("templates", {})]
                tablese["langlinks"] = {fo["lang"]: fo.get("title") or fo.get("*") or "" for fo in caca.get("langlinks", [])}
                # ---
                table[cate_title] = tablese
            # ---
        return table

    def add_to_result_table(self, x, tab):
        if x in self.result_table:
            return

        if self.without_lang != "":
            no_langs = tab.get("langlinks", {}).get(self.without_lang, "")
            if no_langs != "":
                return

        if self.with_lang != "":
            langs = tab.get("langlinks", {}).get(self.with_lang, "")
            if langs == "":
                return
        # print(tab)
        self.result_table[x] = tab

    def subcatquery_(self):
        # ---
        print(f"catdepyh_new.py cat:{self.title}, ns:{self.ns}")
        # ---
        tablemember = self.get_cat(self.title)
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
            for cat in new_list:
                # ---
                table2 = self.get_cat(cat)
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


def subcatquery(title, sitecode="en", family="wikipedia", depth=0, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[], **kwargs):
    # ---
    priffixs = {"ar": "تصنيف:", "en": "Category:"}
    # ---
    start_priffix = priffixs.get(sitecode)
    # ---
    if start_priffix and not title.startswith(start_priffix):
        title = start_priffix + title
    # ---
    printe.output(f"<<lightyellow>> catdepth_new.py sub cat query for {sitecode}:{title}, depth:{depth}, ns:{ns}")
    # ---
    start = time.time()
    final = time.time()
    # ---
    bot = CategoryDepth(title, sitecode=sitecode, family=family, depth=depth, ns=ns, nslist=nslist, without_lang=without_lang, with_lang=with_lang, tempyes=tempyes, **kwargs)
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


def login_wiki(sitecode="en", family="wikipedia"):
    # ---
    bot = CategoryDepth("", sitecode=sitecode, family=family)
    # ---
    bot.log.Log_to_wiki_1()
