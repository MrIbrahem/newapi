'''

python3 core8/pwb.py newapi/tests/test_bot_api test:4
python3 core8/pwb.py newapi/tests/test_bot_api test:44
python3 core8/pwb.py newapi/tests/test_bot_api noprr test:9

'''
import sys
import time

from newapi.page import NEW_API
from newapi.page import NEW_API

from newapi import printe

sys.argv.append("printurl")
# ---


class testmybot:

    def __init__(self):
        self.test = "test"
        self.api_new = NEW_API('ar', family='wikipedia')
        # self.api_new.Login_to_wiki()

    def test1(self):
        '''Find_pages_exists_or_not'''
        ex = self.api_new.Find_pages_exists_or_not(["اليمن", "sana'a"])
        return ex

    def test2(self):
        '''Get_All_pages'''
        ex = self.api_new.Get_All_pages(start='!', limit_all=10000)
        return ex

    def test3(self):
        '''Search'''
        ex = self.api_new.Search('yemen', srlimit="1000")
        return ex

    def test4(self):
        '''Get_Newpages'''
        ex = self.api_new.Get_Newpages(limit=10000)
        return ex

    def test5(self):
        '''Get_langlinks_for_list'''
        ex = self.api_new.Get_langlinks_for_list(["طواف العالم للدراجات 2023", "كريس فروم"])
        return ex

    def test6(self):
        '''UserContribs'''
        ex = self.api_new.UserContribs('User:Mr. Ibahem', limit="10", namespace="*", ucshow="")
        return ex

    def test7(self):
        '''expandtemplates'''
        ex = self.api_new.expandtemplates('{{refn|Wing drop is an unc maneuvering.}}')
        return ex

    def test8(self):
        '''get_extlinks'''
        ex = self.api_new.get_extlinks('اليمن')
        return ex
    def test9(self):
        '''querypage_list'''
        ex = self.api_new.querypage_list(qppage='Wantedcategories', Max=500)
        return ex

    def test10(self):
        '''Get_template_pages'''
        ex = self.api_new.Get_template_pages( "قالب:طواف العالم للدراجات", namespace="*", Max=10000)
        return ex

    def start(self):
        # ---
        defs1 = {}
        # ---
        defs = {
            1: self.test1,
            2: self.test2,
            3: self.test3,
            4: self.test4,
            5: self.test5,
            6: self.test6,
            7: self.test7,
            8: self.test8,
            9: self.test9,
            10: self.test10
        }
        # ---
        for arg in sys.argv:
            arg, _, value = arg.partition(":")
            if arg == "test" and value.isdigit():
                d = int(value)
                defs1[d] = defs[d]
        # ---
        if defs1 != {}:
            defs = defs1
        # ---
        for n, func in defs.items():
            name = func.__name__
            printe.output(f"<<lightgreen>> start def number {n}, name:{name}:")
            # ---
            def_name = func.__doc__
            printe.output(f"<<lightyellow>> test: {def_name}:")
            # ---
            if "tat" in sys.argv:
                continue
            # ---
            result = func()
            # ---
            # printe.output( result )
            # ---
            if isinstance(result, dict):
                for na, ta in result.items():
                    na2 = na  # f" '{na}' ".ljust(10)
                    # ---
                    if na == "claims":
                        for x, u in ta.items():
                            ta = {
                                x: u
                            }
                            break
                    # ---
                    # ta = json.dumps(ta, indent=2, ensure_ascii=False)
                    # ---
                    printe.output(f"* {na2}: {ta}")
            # ---
            if result == "":
                raise Exception("result == ''")
            # ---
            if "noprr" not in sys.argv:
                if isinstance(result, str):
                    printe.output(f"result:{result}")
                elif isinstance(result, list):
                    printe.output(result)
                else:
                    printe.output(result)
            # ---
            printe.output(f"{len(result)=}")
            printe.output("=====================")
            printe.output(f"<<lightyellow>> test: {def_name} end...")
            printe.output("time.sleep(1)")
            time.sleep(1)


# ---
if __name__ == '__main__':
    testmybot().start()
# ---
