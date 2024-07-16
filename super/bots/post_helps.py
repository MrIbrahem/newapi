"""
from newapi.super.bots.post_helps import POST_HELPS

"""
import sys
from newapi import printe

yes_answer = ["y", "a", "", "Y", "A", "all", "aaa"]
Save_Edit_Pages = {1: False}
file_name = "bot_api.py"


def test_print(s):
    if "test_print" in sys.argv:
        printe.output(s)

class POST_HELPS:
    def __init__(self):
        printe("class POST_HELPS:")
        pass

    def post_continue(self, params, action, _p_="pages", p_empty=None, Max=500000, first=False, _p_2="", _p_2_empty=None):
        # ---
        if not isinstance(Max, int) and Max.isdigit():
            Max = int(Max)
        # ---
        if Max == 0:
            Max = 500000
        # ---
        p_empty = p_empty or []
        _p_2_empty = _p_2_empty or []
        # ---
        results = p_empty
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
                test_print("post continue, data is empty. break")
                break
            # ---
            test_print(f"post continue, len:{len(data)}, all: {len(results)}")
            # ---
            if Max <= len(results) and len(results) > 1:
                test_print(f"post continue, {Max=} <= {len(results)=}. break")
                break
            # ---
            if isinstance(results, list):
                results.extend(data)
            else:
                print(f"{type(results)=}")
                print(f"{type(data)=}")
                results = {**results, **data}
        # ---
        test_print(f"post continue, {len(results)=}")
        # ---
        return results
