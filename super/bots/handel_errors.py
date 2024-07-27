"""
from newapi.super.bots.handel_errors import HANDEL_ERRORS

"""
import sys
from newapi import printe


class HANDEL_ERRORS:
    def __init__(self):
        printe("class HANDEL_ERRORS:")
        pass

    def handel_err(self, error: dict, function: str = "", params: dict = None, do_error: bool = True):
        # ---
        # {'error': {'code': 'articleexists', 'info': 'The article you tried to create has been created already.', '*': 'See https://ar.wikipedia.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/postorius/lists/mediawiki-api-announce.lists.wikimedia.org/&gt; for notice of API deprecations and breaking changes.'}, 'servedby': 'mw1425'}
        # ---
        err_code = error.get("code", "")
        err_info = error.get("info", "")
        # ---
        tt = f"<<lightred>>{function} ERROR: <<defaut>>code:{err_code}."
        # printe.output(tt)
        # warn(warn_err(tt), UserWarning)
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
        if err_code == "no-such-entity":
            printe.output("<<lightred>> ** no-such-entity. ")
            return False
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
        if err_code == "maxlag":
            printe.output("<<lightred>> ** maxlag. ")
            return False
        # ---
        if do_error:
            printe.output(f"<<lightred>>{function} ERROR: <<defaut>>info: {err_info}, {params=}")
        # ---
        if "raise" in sys.argv:
            raise Exception(error)
