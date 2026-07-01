import sys
import os
from textwrap import dedent
import urllib.parse
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from ext.slugs import slugify

def on_pre_build(config):
    for plugin in config.plugins:
        if plugin.__class__.__name__ == "BlogPlugin":
            plugin.config.post_slugify = slugify(short=True)
            break
    return config


x_intent = "https://twitter.com/intent/tweet"
fb_sharer = "https://www.facebook.com/sharer/sharer.php"
whatsapp = "https://wa.me"
telegram = "https://t.me/share/url"
include = re.compile(r"blog/[1-9].*")


def on_page_markdown(markdown, **kwargs):
    page = kwargs["page"]
    config = kwargs["config"]
    if not include.match(page.url):
        return markdown

    page_url = config.site_url + page.url
    page_title = urllib.parse.quote(page.title + "\n")

    return markdown + dedent(f"""
    [Compartilhar no :simple-whatsapp:]({whatsapp}?text={page_title + urllib.parse.quote(page_url)}){{ .md-button }}
    [Compartilhar no :simple-telegram:]({telegram}?url={page_url}&text={page_title}){{ .md-button }}
    [Compartilhar no :simple-x:]({x_intent}?text={page_title}&url={page_url}){{ .md-button }}
    """)

    # [Compartilhar no :simple-facebook:]({fb_sharer}?u={page_url}){{ .md-button }}
