"""

from newapi.super.botapi_bots.bot import BOTS_APIS

"""
import sys
import pywikibot
from newapi import printe
from newapi.super.bots.post_helps import POST_HELPS
from newapi.super.bots.handel_errors import HANDEL_ERRORS

yes_answer = ["y", "a", "", "Y", "A", "all", "aaa"]
Save_Edit_Pages = {1: False}
file_name = "bot_api.py"


def test_print(s):
    if "test_print" in sys.argv:
        printe.output(s)


class BOTS_APIS(POST_HELPS, HANDEL_ERRORS):
    def __init__(self):
        # print("class APIS:")
        self.username = ""
        super().__init__()

    def ask_put(self, nodiff=False, newtext="", text=""):
        yes_answer = ["y", "a", "", "Y", "A", "all", "aaa"]
        # ---
        if "ask" in sys.argv and not Save_Edit_Pages[1]:
            # ---
            if "nodiff" not in sys.argv and not nodiff:
                if len(newtext) < 70000 and len(text) < 70000 or "diff" in sys.argv:
                    printe.showDiff(text, newtext)
                else:
                    printe.output("showDiff error..")
                    printe.output(f"diference in bytes: {len(newtext) - len(text)}")
                    printe.output(f"length of text: {len(text)}, length of newtext: {len(newtext)}")
            # ---
            sa = pywikibot.input(f"<<lightyellow>>bot_api.py: save (yes, no)? {self.username=}")
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
        test_print(f"** Add_To_Bottom2 .. [[{title}]] ")
        # printe.showDiff("", text)
        # ---
        ask = self.ask_put(newtext=text, text="")
        # ---
        if ask is False:
            return False
        # ---
        params = {
            "action": "edit",
            "format": "json",
            "title": title,
            "summary": summary,
            "notminor": 1,
            "nocreate": 1,
            "utf8": 1,
        }
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
        data = results.get("edit", {})
        result = data.get("result", "")
        # ---
        if result == "Success":
            printe.output("<<lightgreen>>** true.")
            return True
        # ---
        error = results.get("error", {})
        # ---
        if error != {}:
            print(results)
            er = self.handel_err(error, function="Add_To_Bottom", params=params)
            # ---
            return er
        # ---
        return True

    def move(self, old_title, to, reason="", noredirect=False, movesubpages=False):
        # ---
        printe.output(f"<<lightyellow>> def move [[{old_title}]] to [[{to}]] ")
        # ---
        params = {
            "action": "move",
            "format": "json",
            "from": old_title,
            "to": to,
            "movetalk": 1,
            "formatversion": 2,
        }
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
            test_print(f"<<lightred>>** old_title == to {to} ")
            return False
        # ---
        if not self.save_move and "ask" in sys.argv:
            sa = pywikibot.input(f"<<lightyellow>>bot_api: Do you move page:[[{old_title}]] to [[{to}]]? ([y]es, [N]o, [a]ll)? {self.username=}")
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
            test_print(f"<<lightgreen>> answer: {sa in yes_answer}")
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

    def expandtemplates(self, text):
        # ---
        params = {
            "action": "expandtemplates",
            "format": "json",
            "text": text,
            "prop": "wikitext",
            "formatversion": 2,
        }
        # ---
        data = self.post_params(params)
        # ---
        if not data:
            return text
        # ---
        newtext = data.get("expandtemplates", {}).get("wikitext") or text
        # ---
        return newtext

    def Parse_Text(self, line, title):
        # ---
        params = {
            "action": "parse",
            "prop": "wikitext",
            "text": line,
            "title": title,
            "pst": 1,
            "contentmodel": "wikitext",
            "utf8": 1,
            "formatversion": 2,
        }
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
