#!/usr/bin/python3
"""

from newapi import txtlib
# txtlib.get_one_temp_params( text, templates=[], lowers=False )
# alltemp = txtlib.get_all_temps_params( text, templates=[], lowers=False )
# for tab in alltemp: for namestrip, params in tab.keys():
# ---
from newapi import txtlib
# temps = txtlib.extract_templates_and_params(text)
# for temp in temps: name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']

"""
#
# (C) Ibrahem Qasim, 2021
#
#
# ---
# from newapi import printe

try:
    import wikitextparser
except ImportError:
    print('import wikitextparser error..')
    try:
        import mwparserfromhell as wikitextparser
    except ImportError:
        # print required because pywikibot is not imported completely
        raise ImportError(
            """
Pywikibot is missing a MediaWiki markup parser which is necessary.
Please update the required module with either

    pip install "mwparserfromhell>=0.5.0"

or

    pip install "wikitextparser>=0.47.5"
"""
        ) from None


def extract_templates_and_params(text):
    # ---
    result = []
    # ---
    pra = wikitextparser
    # ---
    '''
    if RECURSE_OTHERS :
        try:
            import mwparserfromhell as pra
            printe.output("mwparserfromhell is used")
        except ImportError:
            printe.output("mwparserfromhell is missing")
            return result
    '''
    # ---
    parser_name = pra.__name__
    parsed = pra.parse(text)
    if parser_name == 'wikitextparser':
        templates = parsed.templates
        arguments = 'arguments'
    else:
        # if RECURSE_OTHERS:
        # templates = parsed.ifilter_templates(parsed.RECURSE_OTHERS, matches=lambda x: not x.name.lstrip().startswith('#'))
        # else:
        templates = parsed.ifilter_templates(matches=lambda x: not x.name.lstrip().startswith('#'), recursive=True)
        arguments = 'params'
    # ---
    # print("parsed.templates:")
    # print(parsed.templates)
    # ---
    for template in templates:
        # print(dir(template))
        # ---
        # params = OrderedDict()
        params = {}
        for param in getattr(template, arguments):
            value = str(param.value)  # mwpfh needs upcast to str
            key = str(param.name)
            key = key.strip()
            params[key] = value
        # ---
        name = template.name.strip()
        # ---
        # print('=====')
        # ---
        if parser_name == 'wikitextparser':
            name = str(template.normal_name()).strip()
            pa_item = template.string
        else:
            pa_item = template.__str__()
        # printe.output( "<<lightyellow>> pa_item: %s" % pa_item )
        # ---
        namestrip = name
        # ---
        ficrt = {
            'name': f"قالب:{name}",
            'namestrip': namestrip,
            'params': params,
            'item': pa_item,
        }
        # ---
        result.append(ficrt)
    # ---
    return result


def get_one_temp_params(text, tempname="", templates=[], lowers=False, get_all_temps=False):
    ingr = extract_templates_and_params(text)
    # ---
    temps = templates
    # ---
    if tempname != '':
        temps.append(tempname)
    # ---
    temps = [x.replace("قالب:", "").replace("Template:", "").replace('_', ' ').strip() for x in temps]
    # ---
    if lowers:
        temps = [x.lower() for x in temps]
    # ---
    named = {}
    # ---
    if get_all_temps:
        named = []
    # ---
    for temp in ingr:
        # ---
        name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']
        # ---
        if lowers:
            namestrip = namestrip.lower()
        # ---
        if namestrip in temps:
            if not get_all_temps:
                return params
            # ---
            # print("te:%s, namestrip:%s" % (te,namestrip) )
            # ---
            tabe = {namestrip: params}
            named.append(tabe)
    # ---
    return named


def get_all_temps_params(text, templates=[], lowers=False):
    tab = get_one_temp_params(text, templates=templates, lowers=lowers, get_all_temps=True)
    return tab


# ---
test_text = '''
{{ص.م/صورة مضاعفة ويكي بيانات|معرف ويكي بيانات={{{معرف ويكي بيانات|}}}
| صورة1 ={{{علم|{{{flag|{{{صورة علم|}}}}}}}}}
| تعليق1 ={{#لو:{{قيمة ويكي بيانات|معرف ويكي بيانات={{{معرف ويكي بيانات|}}}|{{{وصف العلم|{{{flagcaption|}}}}}}|خاصية=P163|rank=best}}|{{قيمة ويكي بيانات|معرف ويكي بيانات={{{معرف ويكي بيانات|}}}|{{{وصف العلم|{{{flagcaption|}}}}}}|خاصية=P163|rank=best}}|{{فصع}}}}
| عرض1 ={{{عرض العلم|{{{flagsize|125}}}}}}
| صورة2 ={{{motto|{{{شعار|}}}}}}
| تعليق2 ={{#لو:{{قيمة ويكي بيانات|معرف ويكي بيانات={{{معرف ويكي بيانات|}}}|{{{تعليق الشعار|{{{وصف الشعار|}}}}}}|خاصية=P237|rank=best}}|{{قيمة ويكي بيانات|معرف ويكي بيانات={{{معرف ويكي بيانات|}}}|{{{تعليق الشعار|{{{وصف الشعار|}}}}}}|خاصية=P237|rank=best}}|{{فصع}}}}
| عرض2 = {{{عرض الشعار|125}}}
| خاصية1 =P41
| خاصية2 ={{#لو:{{#خاصية:P94}}|P94|P154}}
|خلفية={{{خلفية|}}}
}}

{{ourworldindatamirror|https://owidm.wmcloud.org/grapher/cancer-death-rates?tab=map {{Webarchive}}}}
'''
# ---
if __name__ == '__main__':
    # ---
    # ---
    ingr = extract_templates_and_params(test_text)
    for temp in ingr:
        # ---
        name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']
        # ---
        print("-----------------------------")
        print(f"name: {name}")
        print(f"namestrip: {namestrip}")
        print(f"params: {params}")
        print(f"template: {template}")

    # ---
    parser_name = wikitextparser.__name__
    print(f"parser_name: {parser_name}")
