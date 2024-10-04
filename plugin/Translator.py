# -*- coding: utf-8 -*-
"""
youdao Translate in Flowlauncher.

This plugin allows translation using youdao Translate and copy it.

can return multiple results.

You can use it by typing "yd" in Flowlauncher and then typing the word you want to translate.
"""

from flowlauncher import FlowLauncher, FlowLauncherAPI
import urllib.parse
import urllib.request
import json
import subprocess


## https://dict.youdao.com/suggest?num=5&ver=3.0&doctype=json&cache=false&le=en&q=draw
def translate(
    to_translate,
):
    """Get translated query from youdao translate."""
    agent = {"User-Agent": "Edge, Brave, Firefox, Chrome, Opera"}
    base_link = "https://dict.youdao.com/suggest?num=5&ver=3.0&doctype=json&cache=false&le=en&q=%s"
    to_translate = urllib.parse.quote(to_translate)
    link = base_link % to_translate
    request = urllib.request.Request(link, headers=agent)
    raw_data = urllib.request.urlopen(request).read()
    results = json.loads(raw_data.decode("utf-8"))
    if results["result"]["msg"] == "success":
        if results["data"]["entries"]:
            re_result = results["data"]["entries"][0]["explain"].replace("；", ";")

        return re_result.split(";")
    else:
        return ["😥No result"]


def copy2clip(txt):
    """Put translation into clipboard."""
    cmd = "echo " + txt.strip() + "|clip"
    return subprocess.check_call(cmd, shell=True)


class Translate(FlowLauncher):

    def query(self, query):
        results = []
        try:
            urllib.request.urlopen("https://translate.google.com/")
            # Online or Normal workflow
            if len(query.strip()) == 0:
                results.append(
                    {
                        "Title": "😊有道中英文互译",
                        "SubTitle": "youdao translate chn-eng",
                        "IcoPath": "Images/yd.png",
                        "ContextData": "ctxData",
                    }
                )
            else:

                translation = translate(query)
                for item in translation:
                    results.append(
                        {
                            "Title": "译: " + item,
                            "SubTitle": "原: " + query,
                            "IcoPath": "Images/yd.png",
                            "ContextData": "ctxData",
                            "JsonRPCAction": {
                                "method": "copy",
                                "parameters": [item],
                            },
                        }
                    )
        except urllib.error.URLError as e:
            # Offline or input error
            results.append(
                {
                    "Title": e,
                    "SubTitle": "😅出错啦，请检查网络连接或输入",
                    "IcoPath": "Images/yd.png",
                    "ContextData": "ctxData",
                }
            )

        return results

    def copy(self, ans):
        """Copy translation to clipboard."""
        FlowLauncherAPI.show_msg("Copied to clipboard", copy2clip(ans))


if __name__ == "__main__":
    Translate()
