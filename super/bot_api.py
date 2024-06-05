"""
from newapi.page import NEW_API
# api_new  = NEW_API('ar', family='wikipedia')
# login    = api_new.Login_to_wiki()
# move_it  = api_new.move(old_title, to, reason="", noredirect=False, movesubpages=False)
# pages    = api_new.Find_pages_exists_or_not(liste, get_redirect=False)
# json1    = api_new.post_params(params, addtoken=False)
# pages    = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)
# search   = api_new.Search(value='', ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
# newpages = api_new.Get_Newpages(limit="max", namespace="0", rcstart="", user='', three_houers=False)
# usercont = api_new.UserContribs(user, limit=5000, namespace="*", ucshow="")
# l_links  = api_new.Get_langlinks_for_list(titles, targtsitecode="", numbes=50)
# text_w   = api_new.expandtemplates(text)
# subst    = api_new.Parse_Text('{{subst:page_name}}', title)
# extlinks = api_new.get_extlinks(title)
# revisions= api_new.get_revisions(title)
# logs     = api_new.get_logs(title)
# wantedcategories  = api_new.querypage_list(qppage='Wantedcategories|Wantedfiles', qplimit="max", Max=5000)
# pages  = api_new.Get_template_pages(title, namespace="*", Max=10000)
# img_url  = api_new.Get_image_url(title)
# added    = api_new.Add_To_Bottom(text, summary, title, poss="Head|Bottom")

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
import sys
import pywikibot
import datetime
from datetime import timedelta

from newapi import printe

change_codes = {"nb": "no", "bat_smg": "bat-smg", "be_x_old": "be-tarask", "be-x-old": "be-tarask", "cbk_zam": "cbk-zam", "fiu_vro": "fiu-vro", "map_bms": "map-bms", "nds_nl": "nds-nl", "roa_rup": "roa-rup", "zh_classical": "zh-classical", "zh_min_nan": "zh-min-nan", "zh_yue": "zh-yue"}
yes_answer = ["y", "a", "", "Y", "A", "all", "aaa"]
Save_Edit_Pages = { 1: False }

def login_def(lang, family):
    return {}

def test_print(s):
    if "test_print" in sys.argv:
        printe.output(s)


class NEW_API:
    def __init__(self, lang, family="wikipedia"):
        # ---
        self.lang = change_codes.get(lang) or lang
        # ---
        self.save_move = False
        # ---
        self.family = family
        self.endpoint = f"https://{lang}.{family}.org/w/api.php"
        # ---
        self.log = login_def(self.lang, family=self.family)

    def Login_to_wiki(self):
        # ---
        self.log.Log_to_wiki()

    def handel_err(self, error, function):
        # ---
        # {'error': {'code': 'articleexists', 'info': 'The article you tried to create has been created already.', '*': 'See https://ar.wikipedia.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/postorius/lists/mediawiki-api-announce.lists.wikimedia.org/&gt; for notice of API deprecations and breaking changes.'}, 'servedby': 'mw1425'}
        # ---
        err_code = error.get("code", "")
        err_info = error.get("info", "")
        # ---
        printe.output(f"<<lightred>>{function} ERROR: <<defaut>>code:{err_code}.")
        # ---["protectedpage", 'تأخير البوتات 3 ساعات', False]
        if err_code == "abusefilter-disallowed":
            # ---
            # oioioi = {'error': {'code': 'abusefilter-disallowed', 'info': 'This', 'abusefilter': {'id': '169', 'description': 'تأخير البوتات 3 ساعات', 'actions': ['disallow']}, '*': 'See https'}, 'servedby': 'mw1374'}
            # ---
            abusefilter = error.get("abusefilter", "")
            description = abusefilter.get("description", "")
            printe.output(f"<<lightred>> ** abusefilter-disallowed: {description} ")
            if description in ["تأخير البوتات 3 ساعات", "تأخير البوتات 3 ساعات- 3 من 3", "تأخير البوتات 3 ساعات- 1 من 3", "تأخير البوتات 3 ساعات- 2 من 3"]:
                return False
            return description
        # ---
        if err_code == "protectedpage":
            printe.output("<<lightred>> ** protectedpage. ")
            # return "protectedpage"
            return False
        # ---
        if err_code == "articleexists":
            printe.output("<<lightred>> ** article already created. ")
            return "articleexists"
        # ---
        printe.output(f"<<lightred>>{function} ERROR: <<defaut>>info: {err_info}.")

    def post_params(self, params, addtoken=False, files=None):
        return self.log.post(params, addtoken=addtoken, files=files)

    def post_continue(self, params, action, _p_="pages", p_empty=None, Max=50000, first=False, _p_2="", _p_2_empty=None):
        # ---
        if not isinstance(Max, int) and Max.isdigit():
            Max = int(Max)
        # ---
        continue_params = {}
        # ---
        p_empty = p_empty or []
        _p_2_empty = _p_2_empty or []
        # ---
        results = p_empty
        # ---
        while continue_params != {} or len(results) == 0:
            # ---
            if continue_params:
                # params = {**params, **continue_params}
                params.update(continue_params)
            # ---
            json1 = self.post_params(params)
            # ---
            if not json1:
                test_print("post_continue, json1 is empty. break")
                break
            # ---
            continue_params = json1.get("continue", {})
            # ---
            data = json1.get(action, {}).get(_p_, p_empty)
            # ---
            if _p_ == "querypage":
                data = data.get("results", [])
            elif first:
                if isinstance(data, list) and len(data) > 0:
                    data = data[0]
                    if _p_2:
                        data = data.get(_p_2, _p_2_empty)
            # ---
            if not data:
                test_print("post_continue, data is empty. break")
                break
            # ---
            # test_print(f'post_continue, len:{len(data)}, all: {len(results)}')
            # ---
            if Max <= len(results) and len(results) > 1:
                test_print(f"post_continue, {Max=} <= {len(results)=}. break")
                break
            # ---
            if isinstance(results, list):
                results.extend(data)
            else:
                print(f"{type(results)=}")
                print(f"{type(data)=}")
                results = {**results, **data}
        # ---
        test_print(f"post_continue, {len(results)=}")
        # ---
        return results

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
        for i in range(0, len(liste), 50):
            titles = liste[i : i + 50]
            # ---
            done += len(titles)
            # ---
            if not noprint:
                printe.output(f"Find_pages_exists_or_not : {done}/{len(liste)}")
            # ---
            params = {"action": "query", "titles": "|".join(titles), "prop": "info", "formatversion": 2}
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

    def Get_All_pages(self, start="", namespace="0", limit="max", apfilterredir="", limit_all=0):
        # ---
        printe.output(f"Get_All_pages for start:{start}, limit:{limit},namespace:{namespace},apfilterredir:{apfilterredir}")
        # ---
        params = {"action": "query", "format": "json", "list": "allpages", "apnamespace": namespace, "aplimit": limit, "apfilterredir": "nonredirects", "formatversion": 1}
        # ---
        if str(namespace) in ["*", "", "all"]:
            del params["apnamespace"]
        # ---
        if apfilterredir in ["redirects", "all", "nonredirects"]:
            params["apfilterredir"] = apfilterredir
        # ---
        if start:
            params["apfrom"] = start
        # ---
        newp = self.post_continue(params, "query", _p_="allpages", p_empty=[], Max=limit_all)
        # ---
        printe.output(f"<<lightpurple>> --- Get_All_pages : find {len(newp)} pages.")
        # ---
        Main_table = [x["title"] for x in newp]
        # ---
        printe.output(f"len of Main_table {len(Main_table)}.")
        # ---
        printe.output(f"bot_api.py Get_All_pages : find {len(Main_table)} pages.")
        # ---
        return Main_table

    def Search(self, value="", ns="*", offset="", srlimit="max", RETURN_dict=False, addparams=None):
        # ---
        printe.output(f'bot_api.Search for "{value}",ns:{ns}')
        # ---
        if not srlimit:
            srlimit = "max"
        # ---
        params = {"action": "query", "format": "json", "list": "search", "srsearch": value, "srnamespace": 0, "srlimit": srlimit, "formatversion": 1}
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
        printe.output(f'bot_api.Search find "{len(search)}" all result: {len(results)}')
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
        printe.output(f'bot_api.Get_Newpages find "{len(Main_table)}" result. s')
        # ---
        if three_houers:
            arsite = pywikibot.Site("ar", "wikipedia")
            # ---
            Main_table = [pywikibot.Page(arsite, x) for x in Main_table]
            # ---
        # ---
        return Main_table

    def UserContribs(self, user, limit=5000, namespace="*", ucshow=""):
        # ---
        params = {"action": "query", "format": "json", "list": "usercontribs", "ucdir": "older", "ucnamespace": namespace, "uclimit": "max", "ucuser": user, "utf8": 1, "bot": 1, "ucprop": "title", "formatversion": 1}
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
        printe.output(f'bot_api.Get_langlinks_for_list for "{len(titles)} pages". in wiki:{self.lang}')
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
            printe.output(f'params["lllang"] = {targtsitecode}')
        # ---
        find_targtsitecode = 0
        normalized = {}
        table = {}
        # ---
        for i in range(0, len(titles), numbes):
            # ---
            group = titles[i: i + numbes]
            # ---
            # printe.output(f'bot_api.Get_langlinks_for_list work for {len(group)} pages')
            # ---
            params["titles"] = "|".join(group)
            # ---
            json1 = self.post_params(params)
            # ---
            if not json1:
                printe.output('bot_api.Get_langlinks_for_list json1 is empty')
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

    def expandtemplates(self, text):
        # ---
        params = {"action": "expandtemplates", "format": "json", "text": text, "prop": "wikitext", "formatversion": 2}
        # ---
        data = self.post_params(params)
        # ---
        if not data:
            return text
        # ---
        newtext = data.get("expandtemplates", {}).get("wikitext") or text
        # ---
        return newtext

    def get_logs(self, title):
        # ---
        params = {"action": "query", "format": "json", "list": "logevents", "ledir": "newer", "letitle": title, "formatversion": 2}
        # ---
        data = self.post_params(params)
        # ---
        if not data:
            return []
        # ---
        logevents = data.get("query", {}).get("logevents") or []
        # ---
        return logevents

    def Parse_Text(self, line, title):
        # ---
        params = {"action": "parse", "prop": "wikitext", "text": line, "title": title, "pst": 1, "contentmodel": "wikitext", "utf8": 1, "formatversion": 2}
        # ---
        # {"parse": {"title": "كريس فروم", "pageid": 2639244, "wikitext": "{{subst:user:Mr._Ibrahem/line2|Q76|P31}}", "psttext": "\"Q76\":{\n\"P31\":\"إنسان\"\n\n\n\n\n},"}}
        # ---
        data = self.post_params(params)
        # ---
        if not data:
            return ""
        # ---
        textnew = data.get("parse", {}).get("psttext", "")
        # ---
        textnew = textnew.replace("\\n\\n", "")
        # ---
        return textnew

    def get_extlinks(self, title):
        params = {"action": "query", "format": "json", "prop": "extlinks", "titles": title, "utf8": 1, "ellimit": "max", "formatversion": 2}
        # ---
        results = self.post_continue(params, "query", "pages", [], first=True, _p_2="extlinks", _p_2_empty=[])
        # ---
        links = [x["url"] for x in results]
        # ---
        return sorted(set(links))

    def get_revisions(self, title, rvprop="comment|timestamp|user|content|ids", options=None):
        # ---
        params = {"action": "query", "format": "json", "prop": "revisions", "titles": title, "utf8": 1, "rvprop": "comment|timestamp|user|content|ids", "rvdir": "newer", "rvlimit": "max", "formatversion": 2}
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
        Max = Max or 5000
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
        printe.output(f"querypage_list len(results) = {len(results)}")
        # ---
        return results

    def move(self, old_title, to, reason="", noredirect=False, movesubpages=False):
        # ---
        printe.output(f"<<lightyellow>> def move [[{old_title}]] to [[{to}]] ")
        # ---
        params = {"action": "move", "format": "json", "from": old_title, "to": to, "movetalk": 1, "formatversion": 2}
        # ---
        if noredirect:
            params["noredirect"] = 1
        if movesubpages:
            params["movesubpages"] = 1
        # ---
        if reason:
            params["reason"] = reason
        # ---
        if old_title == to:
            printe.output(f"<<lightred>>** old_title == to {to} ")
            return False
        # ---
        if not self.save_move and "ask" in sys.argv:
            sa = pywikibot.input(f"<<lightyellow>>bot_api: Do you move page:[[{old_title}]] to [[{to}]]? ([y]es, [N]o, [a]ll)?")
            # ---
            if sa == "a":
                printe.output("<<lightgreen>> ---------------------------------")
                printe.output("<<lightgreen>> bot_api.py move all without asking.")
                printe.output("<<lightgreen>> ---------------------------------")
                self.save_move = True
            # ---
            if sa not in yes_answer:
                printe.output("<<red>> bot_api: wrong answer")
                return False
            # ---
            printe.output(f"<<lightgreen>> answer: {sa in yes_answer}")
        # ---
        data = self.post_params(params)
        # { "move": { "from": "d", "to": "d2", "reason": "wrong", "redirectcreated": true, "moveoverredirect": false } }
        # ---
        if not data:
            printe.output("no data")
            return ""
        # ---
        _expend_data = {
            "move": {
                "from": "User:Mr. Ibrahem",
                "to": "User:Mr. Ibrahem/x",
                "reason": "wrong title",
                "redirectcreated": True,
                "moveoverredirect": False,
                "talkmove-errors": [{"message": "content-not-allowed-here", "params": ["Structured Discussions board", "User talk:Mr. Ibrahem/x", "main"], "code": "contentnotallowedhere", "type": "error"}, {"message": "flow-error-allowcreation-flow-create-board", "params": [], "code": "flow-error-allowcreation-flow-create-board", "type": "error"}],
                "subpages": {"errors": [{"message": "cant-move-subpages", "params": [], "code": "cant-move-subpages", "type": "error"}]},
                "subpages-talk": {"errors": [{"message": "cant-move-subpages", "params": [], "code": "cant-move-subpages", "type": "error"}]},
            }
        }
        # ---
        move_done = data.get("move", {})
        error = data.get("error", {})
        error_code = error.get("code", "")  # missingtitle
        # ---
        # elif "Please choose another name." in r4:
        # ---
        if move_done:
            printe.output("<<lightgreen>>** true.")
            return True
        # ---
        if error:
            if error_code == "ratelimited":
                printe.output("<<red>> move ratelimited:")
                return self.move(old_title, to, reason=reason, noredirect=noredirect, movesubpages=movesubpages)

            if error_code == "articleexists":
                printe.output("<<red>> articleexists")
                return "articleexists"

            printe.output("<<red>> error")
            printe.output(error)

            return False
        # ---
        return False

    def Get_template_pages(self, title, namespace="*", Max=10000):
        # ---
        printe.output(f'Get_template_pages for template:"{title}", limit:"{Max}",namespace:"{namespace}"')
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
        printe.output(f'Get_image_url for file:"{title}":')
        # ---
        params = {"action": "query", "format": "json", "prop": "imageinfo", "titles": title, "iiprop": "url", "formatversion": "2"}
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

    def ask_put(self, nodiff=False, newtext="", text=""):
        yes_answer = ["y", "a", "", "Y", "A", "all", "aaa"]
        # ---
        if 'ask' in sys.argv and not Save_Edit_Pages[1]:
            # ---
            if "nodiff" not in sys.argv and not nodiff:
                if len(newtext) < 70000 and len(text) < 70000 or 'diff' in sys.argv:
                    printe.showDiff(text, newtext)
                else:
                    printe.output('showDiff error..')
                    printe.output(f'diference in bytes: {len(newtext) - len(text)}')
                    printe.output(f'length of text: {len(text)}, length of newtext: {len(newtext)}')
            # ---
            sa = pywikibot.input('<<lightyellow>>bot_api.py: save (yes, no)?')
            # ---
            if sa == "a":
                printe.output('<<lightgreen>> ---------------------------------')
                printe.output(f'<<lightgreen>> {__file__} save all without asking.')
                printe.output('<<lightgreen>> ---------------------------------')
                Save_Edit_Pages[1] = True
            # ---
            if sa not in yes_answer:
                printe.output("wrong answer")
                return False
        # ---
        return True

    def Add_To_Bottom(self, text, summary, title, poss="Head|Bottom"):
        # ---
        if not title.strip():
            printe.output('** Add_To_Bottom2 ..  title == ""')
            return False
        # ---
        if not text.strip():
            printe.output('** Add_To_Bottom2 ..  text == ""')
            return False
        # ---
        printe.output(f"** Add_To_Bottom2 .. [[{title}]] ")
        # printe.showDiff("", text)
        # ---
        ask = self.ask_put(newtext=text, text="")
        # ---
        if ask is False:
            return False
        # ---
        params = {"action": "edit", "format": "json", "title": title, "summary": summary, "notminor": 1, "nocreate": 1, "utf8": 1}
        # ---
        if poss == "Head":
            params["prependtext"] = f"{text.strip()}\n"
        else:
            params["appendtext"] = f"\n{text.strip()}"
        # ---
        results = self.post_params(params)
        # ---
        if not results:
            return ""
        # ---
        error = results.get("error", {})
        data = results.get("edit", {})
        result = data.get("result", "")
        # ---
        if result == "Success":
            printe.output("<<lightgreen>>** true.")
            return True
        # ---
        if error != {}:
            er = self.handel_err(error, function='Add_To_Bottom')
            # ---
            return er
        # ---
        return True
