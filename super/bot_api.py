"""
from newapi.page import NEW_API
# api_new  = NEW_API('ar', family='wikipedia')
# login    = api_new.Login_to_wiki()
# move_it  = api_new.move(old_title, to, reason="", noredirect=False, movesubpages=False)
# pages    = api_new.Find_pages_exists_or_not(liste, get_redirect=False)
# json1    = api_new.post_params(params, addtoken=False)
# pages    = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)
# pages    = api_new.PrefixSearch(pssearch="", ns="0", pslimit="max", limit_all=100000)
# all_pages= api_new.Get_All_pages_generator(start="", namespace="0", limit="max", filterredir="", ppprop="", limit_all=100000)
# search   = api_new.Search(value='', ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
# newpages = api_new.Get_Newpages(limit="max", namespace="0", rcstart="", user='')
# usercont = api_new.UserContribs(user, limit=5000, namespace="*", ucshow="")
# l_links  = api_new.Get_langlinks_for_list(titles, targtsitecode="", numbes=50)
# text_w   = api_new.expandtemplates(text)
# subst    = api_new.Parse_Text('{{subst:page_name}}', title)
# extlinks = api_new.get_extlinks(title)
# revisions= api_new.get_revisions(title)
# logs     = api_new.get_logs(title)
# wantedcategories  = api_new.querypage_list(qppage='Wantedcategories|Wantedfiles', qplimit="max", Max=5000)
# pages  = api_new.Get_template_pages(title, namespace="*", Max=10000)
# pages_props  = api_new.pageswithprop(pwppropname="unlinkedwikibase_id", Max=None)
# img_url  = api_new.Get_image_url(title)
# added    = api_new.Add_To_Bottom(text, summary, title, poss="Head|Bottom")
# titles   = api_new.get_titles_redirects(titles)
# titles   = api_new.get_pageassessments(titles)
Usage:
from newapi.page import NEW_API
# ---
login_done_lang = {1:''}
# ---
# في بعض البوتات التي يتم ادخال اللغة من خلال وظائف معينة
# ---
if login_done_lang[1] != code:
    login_done_lang[1] = code
    api_new = NEW_API(code, family='wikipedia')
    api_new.Login_to_wiki()
"""
# ---
import tqdm
import sys
import datetime
from datetime import timedelta
from newapi import printe
from newapi.super.botapi_bots.bot import BOTS_APIS
from newapi.super.super_login import Login

User_tables = {}

change_codes = {"nb": "no", "bat_smg": "bat-smg", "be_x_old": "be-tarask", "be-x-old": "be-tarask", "cbk_zam": "cbk-zam", "fiu_vro": "fiu-vro", "map_bms": "map-bms", "nds_nl": "nds-nl", "roa_rup": "roa-rup", "zh_classical": "zh-classical", "zh_min_nan": "zh-min-nan", "zh_yue": "zh-yue"}


def test_print(s):
    if "test_print" in sys.argv:
        printe.output(s)


class NEW_API(Login, BOTS_APIS):
    def __init__(self, lang, family="wikipedia"):
        # ---
        self.username = ""
        # self.family = family
        self.lang = change_codes.get(lang) or lang
        # ---
        super().__init__(lang, family)
        # ---
        self.save_move = False
        # ---
        # self.family = family
        # self.endpoint = f"https://{lang}.{family}.org/w/api.php"
        # ---
        if User_tables != {}:
            for f, tab in User_tables.items():
                self.add_User_tables(f, tab)

    def get_username(self):
        return self.username

    def Login_to_wiki(self):
        # ---
        self.log_to_wiki_1()
        return

    def Find_pages_exists_or_not(self, liste, get_redirect=False, noprint=False):
        # ---
        normalized = {}
        table = {}
        # ---
        done = 0
        # ---
        redirects = 0
        missing = 0
        exists = 0
        # ---
        if noprint:
            qua = range(0, len(liste), 50)
        else:
            qua = tqdm.tqdm(range(0, len(liste), 50))
        # ---
        for i in qua:
            titles = liste[i : i + 50]
            # ---
            done += len(titles)
            # ---
            params = {
                "action": "query",
                "titles": "|".join(titles),
                "prop": "info",
                "formatversion": 2,
            }
            # ---
            json1 = self.post_params(params)
            # ---
            if not json1:
                if not noprint:
                    printe.output("<<lightred>> error when Find_pages_exists_or_not")
                # return table
                continue
            # ---
            query = json1.get("query", {})
            normalz = query.get("normalized", [])
            # ---
            for red in normalz:
                normalized[red["to"]] = red["from"]
            # ---
            query_pages = query.get("pages", [])
            # ---
            for kk in query_pages:
                # ---
                if isinstance(query_pages, dict):
                    kk = query_pages[kk]
                # ---
                tit = kk.get("title", "")
                if tit:
                    tit = normalized.get(tit, tit)
                    # ---
                    table[tit] = True
                    # ---
                    if "missing" in kk:
                        table[tit] = False
                        missing += 1
                    elif "redirect" in kk and get_redirect:
                        table[tit] = "redirect"
                        redirects += 1
                    else:
                        exists += 1
        # ---
        if not noprint:
            printe.output(f"Find_pages_exists_or_not : missing:{missing}, exists: {exists}, redirects: {redirects}")
        # ---
        return table

    def Get_All_pages(self, start="", namespace="0", limit="max", apfilterredir="", ppprop="", limit_all=100000):
        # ---
        test_print(f"Get_All_pages for start:{start}, limit:{limit},namespace:{namespace},apfilterredir:{apfilterredir}")
        # ---
        params = {
            "action": "query",
            "format": "json",
            "prop": "pageprops",
            "list": "allpages",
            "apnamespace": namespace,
            "aplimit": limit,
            "apfilterredir": "nonredirects",
            "formatversion": 1,
        }
        # ---
        if str(namespace) in ["*", "", "all"]:
            del params["apnamespace"]
        # ---
        if ppprop:
            params["ppprop"] = ppprop
        # ---
        if apfilterredir in ["redirects", "all", "nonredirects"]:
            params["apfilterredir"] = apfilterredir
        # ---
        if start:
            params["apfrom"] = start
        # ---
        newp = self.post_continue(params, "query", _p_="allpages", p_empty=[], Max=limit_all)
        # ---
        test_print(f"<<lightpurple>> --- Get_All_pages : find {len(newp)} pages.")
        # ---
        Main_table = [x["title"] for x in newp]
        # ---
        test_print(f"len of Main_table {len(Main_table)}.")
        # ---
        printe.output(f"bot_api.py Get_All_pages : find {len(Main_table)} pages.")
        # ---
        return Main_table

    def PrefixSearch(self, pssearch="", ns="0", pslimit="max", limit_all=100000):
        # ---
        test_print(f"PrefixSearch for start:{pssearch}, pslimit:{pslimit}, ns:{ns}")
        # ---
        pssearch = pssearch.strip() if pssearch else ""
        # ---
        if not pssearch:
            return
        # ---
        params = {
            "action": "query",
            "list": "prefixsearch",
            "pssearch": pssearch,
            "psnamespace": "*",
            "pslimit": "max",
            "formatversion": "1",
            "format": "json",
        }
        # ---
        if str(ns) in ["*", "", "all"]:
            del params["apnamespace"]
        # ---
        if ns.isdigit():
            params["psnamespace"] = ns
        # ---
        if pslimit.isdigit():
            params["pslimit"] = pslimit
        # ---
        newp = self.post_continue(params, "query", _p_="prefixsearch", p_empty=[], Max=limit_all)
        # ---
        test_print(f"<<lightpurple>> --- PrefixSearch : find {len(newp)} pages.")
        # ---
        Main_table = [x["title"] for x in newp]
        # ---
        test_print(f"len of Main_table {len(Main_table)}.")
        # ---
        printe.output(f"bot_api.py PrefixSearch : find {len(Main_table)} pages.")
        # ---
        return Main_table

    def Get_All_pages_generator(self, start="", namespace="0", limit="max", filterredir="", ppprop="", limit_all=100000):
        # ---
        test_print(f"Get_All_pages_generator for start:{start}, limit:{limit},namespace:{namespace},filterredir:{filterredir}")
        # ---
        params = {
            "action": "query",
            "format": "json",
            "prop": "pageprops",
            "generator": "allpages",
            "gapnamespace": namespace,
            "gaplimit": limit,
            "formatversion": 2,
            # "ppprop": "unlinkedwikibase_id",
            "utf8": 1,
        }
        # ---
        if str(namespace) in ["*", "", "all"]:
            del params["gapnamespace"]
        # ---
        if ppprop:
            params["ppprop"] = ppprop
        # ---
        if filterredir in ["redirects", "all", "nonredirects"]:
            params["gapfilterredir"] = filterredir
        # ---
        if start:
            params["gapfrom"] = start
        # ---
        newp = self.post_continue(params, "query", _p_="pages", p_empty=[], Max=limit_all)
        # ---
        test_print(f"<<lightpurple>> --- Get_All_pages_generator : find {len(newp)} pages.")
        # ---
        Main_table = {x["title"]: x for x in newp}
        # ---
        test_print(f"len of Main_table {len(Main_table)}.")
        # ---
        printe.output(f"bot_api.py Get_All_pages_generator : find {len(Main_table)} pages.")
        # ---
        return Main_table

    def Search(self, value="", ns="*", offset="", srlimit="max", RETURN_dict=False, addparams=None):
        # ---
        test_print(f'bot_api.Search for "{value}",ns:{ns}')
        # ---
        if not srlimit:
            srlimit = "max"
        # ---
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": value,
            "srnamespace": 0,
            "srlimit": srlimit,
            "formatversion": 1,
        }
        # ---
        if ns:
            params["srnamespace"] = ns
        # ---
        if offset:
            params["sroffset"] = offset
        # ---
        if addparams:
            addparams = {x: v for x, v in addparams.items() if v and x not in params}
            params = {**params, **addparams}
        # ---
        search = self.post_continue(params, "query", _p_="search", p_empty=[])
        # ---
        results = []
        # ---
        for pag in search:
            if RETURN_dict:
                results.append(pag)
            else:
                results.append(pag["title"])
        # ---
        test_print(f'bot_api.Search find "{len(search)}" all result: {len(results)}')
        # ---
        return results

    def Get_Newpages(self, limit=5000, namespace="0", rcstart="", user="", three_houers=False):
        if three_houers:
            dd = datetime.datetime.utcnow() - timedelta(hours=3)
            rcstart = dd.strftime("%Y-%m-%dT%H:%M:00.000Z")

        params = {
            "action": "query",
            "format": "json",
            "list": "recentchanges",
            "rcnamespace": namespace,
            "rclimit": "max",
            "utf8": 1,
            "rctype": "new",
            "formatversion": 2,
        }

        if rcstart:
            params["rcstart"] = rcstart
        if user:
            params["rcuser"] = user

        if (isinstance(limit, str) and limit.isdigit()) or isinstance(limit, int):
            limit = int(limit)
            params["rclimit"] = limit
        else:
            limit = 5000

        json1 = self.post_continue(params, "query", _p_="recentchanges", p_empty=[], Max=limit)

        Main_table = [x["title"] for x in json1]

        test_print(f'bot_api.Get_Newpages find "{len(Main_table)}" result. s')

        return Main_table

    def UserContribs(self, user, limit=5000, namespace="*", ucshow=""):
        # ---
        params = {
            "action": "query",
            "format": "json",
            "list": "usercontribs",
            "ucdir": "older",
            "ucnamespace": namespace,
            "uclimit": "max",
            "ucuser": user,
            "utf8": 1,
            # "bot": 1,
            "ucprop": "title",
            "formatversion": 1,
        }
        # ---
        if ucshow:
            params["ucshow"] = ucshow
        # ---
        results = self.post_continue(params, "query", _p_="usercontribs", p_empty=[], Max=limit)
        # ---
        results = [x["title"] for x in results]
        # ---
        return results

    def Get_langlinks_for_list(self, titles, targtsitecode="", numbes=40):
        # ---
        test_print(f'bot_api.Get_langlinks_for_list for "{len(titles)} pages". in wiki:{self.lang}')
        # ---
        if targtsitecode.endswith("wiki"):
            targtsitecode = targtsitecode[:-4]
        # ---
        #  error: {'code': 'toomanyvalues', 'info': 'Too many values supplied for parameter "titles". The limit is 50.', 'parameter': 'titles', 'limit': 50, 'lowlimit': 50, 'highlimit': 500, '*': ''}
        # if self.lang != "ar":
        numbes = 50
        # ---
        params = {
            "action": "query",
            "format": "json",
            "prop": "langlinks",
            # "redirects":1,
            # "normalize": 1,
            "lllimit": "max",
            "utf8": 1,
            "formatversion": 1,
        }
        # ---
        if targtsitecode:
            params["lllang"] = targtsitecode
            test_print(f'params["lllang"] = {targtsitecode}')
        # ---
        find_targtsitecode = 0
        normalized = {}
        table = {}
        # ---
        for i in range(0, len(titles), numbes):
            # ---
            group = titles[i : i + numbes]
            # ---
            # test_print(f'bot_api.Get_langlinks_for_list work for {len(group)} pages')
            # ---
            params["titles"] = "|".join(group)
            # ---
            json1 = self.post_params(params)
            # ---
            if not json1:
                printe.output("bot_api.Get_langlinks_for_list json1 is empty")
                continue
            # ---
            _error = json1.get("error", {})
            # ---
            # print("json1:")
            # print(json1)
            # ---
            norma = json1.get("query", {}).get("normalized", {})
            # ---
            for red in norma:
                normalized[red["to"]] = red["from"]
            # ---
            query_pages = json1.get("query", {}).get("pages", {})
            # ---
            for _, kk in query_pages.items():
                titlle = kk.get("title", "")
                # ---
                titlle = normalized.get(titlle, titlle)
                # ---
                table[titlle] = {}
                # ---
                for lang in kk.get("langlinks", []):
                    table[titlle][lang["lang"]] = lang["*"]
                    # ---
                    if lang["lang"] == targtsitecode:
                        find_targtsitecode += 1
        # ---
        printe.output(f'bot_api.Get_langlinks_for_list find "{len(table)}" in table,find_targtsitecode:{targtsitecode}:{find_targtsitecode}')
        # ---
        return table

    def get_logs(self, title):
        # ---
        params = {
            "action": "query",
            "format": "json",
            "list": "logevents",
            "ledir": "newer",
            "letitle": title,
            "formatversion": 2,
        }
        # ---
        data = self.post_params(params)
        # ---
        if not data:
            return []
        # ---
        logevents = data.get("query", {}).get("logevents") or []
        # ---
        return logevents

    def get_extlinks(self, title):
        params = {
            "action": "query",
            "format": "json",
            "prop": "extlinks",
            "titles": title,
            "utf8": 1,
            "ellimit": "max",
            "formatversion": 2,
        }
        # ---
        results = self.post_continue(params, "query", "pages", [], first=True, _p_2="extlinks", _p_2_empty=[])
        # ---
        links = [x["url"] for x in results]
        # ---
        return sorted(set(links))

    def get_pageassessments(self, titles):
        if isinstance(titles, list):
            titles = "|".join(titles)
        # ---
        params = {
            "action": "query",
            "format": "json",
            "prop": "pageassessments",
            "titles": titles,
            "utf8": 1,
            "ellimit": "max",
            "formatversion": 2,
        }
        # ---
        results = self.post_continue(params, "query", "pages", [], first=False, _p_2="pageassessments", _p_2_empty=[])
        # ---
        return results

    def get_revisions(self, title, rvprop="comment|timestamp|user|content|ids", options=None):
        # ---
        params = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": title,
            "utf8": 1,
            "rvprop": "comment|timestamp|user|content|ids",
            "rvdir": "newer",
            "rvlimit": "max",
            "formatversion": 2,
        }
        # ---
        params["rvprop"] = rvprop or "comment|timestamp|user|content|ids"
        # ---
        if options:
            params.update(options)
        # ---
        results = self.post_continue(params, "query", _p_="pages", p_empty=[])
        # ---
        return results

    def querypage_list(self, qppage="Wantedcategories", qplimit=None, Max=None):
        # ---
        params = {
            "action": "query",
            "format": "json",
            "list": "querypage",
            # "qppage": "Wantedcategories",
            "qplimit": "max",
            "formatversion": 2,
        }
        # ---
        if qplimit.isdigit():
            params["qplimit"] = qplimit
        # ---
        params["qppage"] = qppage
        # ---
        qppage_values = [
            "Ancientpages",
            "BrokenRedirects",
            "Deadendpages",
            "DisambiguationPageLinks",
            "DisambiguationPages",
            "DoubleRedirects",
            "Fewestrevisions",
            "GadgetUsage",
            "GloballyWantedFiles",
            "ListDuplicatedFiles",
            "Listredirects",
            "Lonelypages",
            "Longpages",
            "MediaStatistics",
            "MostGloballyLinkedFiles",
            "Mostcategories",
            "Mostimages",
            "Mostinterwikis",
            "Mostlinked",
            "Mostlinkedcategories",
            "Mostlinkedtemplates",
            "Mostrevisions",
            "OrphanedTimedText",
            "Shortpages",
            "Uncategorizedcategories",
            "Uncategorizedimages",
            "Uncategorizedpages",
            "Uncategorizedtemplates",
            "UnconnectedPages",
            "Unusedcategories",
            "Unusedimages",
            "Unusedtemplates",
            "Unwatchedpages",
            "Wantedcategories",
            "Wantedfiles",
            "Wantedpages",
            "Wantedtemplates",
            "Withoutinterwiki",
        ]
        # ---
        if qppage not in qppage_values:
            printe.output(f"<<lightred>> qppage {qppage} not in qppage_values.")
        # ---
        results = self.post_continue(params, "query", _p_="querypage", p_empty=[], Max=Max)
        # ---
        test_print(f"querypage_list len(results) = {len(results)}")
        # ---
        return results

    def Get_template_pages(self, title, namespace="*", Max=10000):
        # ---
        test_print(f'Get_template_pages for template:"{title}", limit:"{Max}",namespace:"{namespace}"')
        # ---
        params = {
            "action": "query",
            # "prop": "info",
            "titles": title,
            "generator": "transcludedin",
            "gtinamespace": namespace,
            "gtilimit": "max",
            "formatversion": "2",
        }
        # ---
        results = self.post_continue(params, "query", _p_="pages", p_empty=[])
        # ---
        # { "pageid": 2973452, "ns": 100, "title": "بوابة:سباق الدراجات الهوائية" }
        pages = [x["title"] for x in results]
        # ---
        printe.output(f"mdwiki_api.py Get_template_pages : find {len(pages)} pages.")
        # ---
        return pages

    def Get_image_url(self, title):
        # ---
        if not title.startswith("File:"):
            title = f"File:{title}"
        # ---
        test_print(f'Get_image_url for file:"{title}":')
        # ---
        params = {
            "action": "query",
            "format": "json",
            "prop": "imageinfo",
            "titles": title,
            "iiprop": "url",
            "formatversion": "2",
        }
        # ---
        results = self.post_params(params)
        # ---
        if not results:
            return ""
        # ---
        data = results.get("query", {}).get("pages", [])
        # ---
        if data:
            data = data[0]
        # ---
        url = data.get("imageinfo", [{}])[0].get("url", "")
        # ---
        printe.output(f"Get_image_url: image url: {url}")
        # ---
        return url

    def pageswithprop(self, pwppropname="unlinkedwikibase_id", pwplimit=None, Max=None):
        # ---
        params = {
            "action": "query",
            "format": "json",
            "list": "pageswithprop",
            "utf8": 1,
            "formatversion": "2",
            "pwplimit": "max",
            "pwppropname": "unlinkedwikibase_id",
            "pwpprop": "title|value",
        }
        # ---
        if pwplimit and pwplimit.isdigit():
            params["pwplimit"] = pwplimit
        # ---
        if pwppropname != "":
            params["pwppropname"] = pwppropname
        # ---
        results = self.post_continue(params, "query", _p_="pageswithprop", p_empty=[], Max=Max)
        # ---
        test_print(f"pageswithprop len(results) = {len(results)}")
        # ---
        return results

    def get_titles_redirects(self, titles):
        # ---
        redirects = {}
        # ---
        for i in range(0, len(titles), 50):
            group = titles[i : i + 50]
            # ---
            params = {
                "action": "query",
                "format": "json",
                "titles": "|".join(group),
                "redirects": 1,
                # "prop": "templates|langlinks",
                "utf8": 1,
                # "normalize": 1,
            }
            # ---
            json1 = self.post_continue(params, "query", _p_="redirects", p_empty=[])
            # ---
            lists = {x["from"]: x["to"] for x in json1}
            # ---
            if lists:
                redirects.update(lists)
        # ---
        return redirects
