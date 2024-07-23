"""
Usage:
from newapi.super import bot_wd

"""
# ---
import sys
import datetime
from datetime import timedelta
from newapi import printe
from newapi.super.super_login import Login
from newapi.super.bots.handel_errors import HANDEL_ERRORS

User_tables = {}


def test_print(s):
    if "test_print" in sys.argv:
        printe.output(s)


class WD_API(Login, HANDEL_ERRORS):
    def __init__(self, lang, family="wikidata"):
        # ---
        self.username = ""
        # ---
        super().__init__(lang, family)
        # ---
        self.lang = lang
        # ---
        self.save_move = False
        # ---
        self.family = "wikidata"
        # ---
        if User_tables != {}:
            for f, tab in User_tables.items():
                self.add_User_tables(f, tab)

    def get_username(self):
        return self.username

    def Login_to_wiki(self):
        # ---
        self.log_to_wiki_1()

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
        # ---
        if three_houers:
            dd = datetime.datetime.utcnow() - timedelta(hours=3)
            # ---
            rcstart = dd.strftime("%Y-%m-%dT%H:%M:00.000Z")
        # ---
        params = {
            "action": "query",
            "format": "json",
            "list": "recentchanges",
            # "rcdir": "newer",
            "rcnamespace": namespace,
            "rclimit": "max",
            "utf8": 1,
            "rctype": "new",
            "formatversion": 2,
        }
        # ---
        if rcstart:
            params["rcstart"] = rcstart
        if user:
            params["rcuser"] = user
        # ---
        if (isinstance(limit, str) and limit.isdigit()) or isinstance(limit, int):
            limit = int(limit)
            params["rclimit"] = limit
        else:
            limit = 5000
        # ---
        json1 = self.post_continue(params, "query", _p_="recentchanges", p_empty=[], Max=limit)
        # ---
        Main_table = [x["title"] for x in json1]
        # ---
        test_print(f'bot_api.Get_Newpages find "{len(Main_table)}" result. s')
        # ---
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
