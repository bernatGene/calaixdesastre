from pathlib import Path
from requests.exceptions import ReadTimeout
from datetime import datetime
from tqdm import tqdm
import yaml
import wikipediaapi
import langcodes
import sqlite3
import pandas as pd

db_file = Path("places.sqlite")

con = sqlite3.connect(db_file)
cur = con.cursor()
res = cur.execute("""
    SELECT 
    title, url, visit_count, last_visit_date
    FROM
    moz_places
    WHERE url like '%wikipedia%';
""")
tuples = res.fetchall()
df = pd.DataFrame(tuples, columns=[
    "title", "url", "visit_count","last_visit_date" 
],)

from urllib.parse import unquote

def get_page_names(urls):
    names = {}
    langs = {}
    lvds = {}
    for url in urls:
        lvd = df[df["url"] == url]['last_visit_date']
        print(lvd, url)
        lvd = datetime.fromtimestamp(lvd.values[0] / 1000000).strftime("%Y-%m-%d-%a")
        print(lvd)
        name = unquote(url).split("/")[-1].replace("_", " ")
        language = unquote(url).split("wikipedia.org")[0].split("/")[-1][:-1]
        try:
            lang_name = langcodes.get(language).describe('en')["language"]
        except langcodes.LanguageTagError:
            continue

        print(url, language, lang_name)
        if name.startswith("File:"):
            continue
        if any(char in name for char in "%?=:"):
            continue
        if "#" in name:
            name = name[0:name.find("#")]

        names[name] = url
        langs[name] = (language, lang_name)
        lvds[name] = lvd
    return names, langs, lvds

page_names, langs, ldvs = get_page_names(df["url"])
print(list(page_names.keys()))


all_langs = {lang for lang, _ in langs.values()}
wikis = {lang : wikipediaapi.Wikipedia('ShamefulBot/0.1 bot (; bernatskrabec@gmail.com)', lang) for lang in all_langs}


def create_md_page(page_name: str, lang, skip_exist=True):
    file_name = Path("mds") / (page_name + ".md")
    if file_name.exists():
        return
    lang_code, lang_name = lang
    page = page_name.replace(" ", "_")
    page = wikis[lang_code].page(page, lang_code)
    if not page.exists():
        print("Can't find page", page_name, lang)
        return
    summary = page.summary
    url = page_names[page_name]
    links = (page.links.keys())
    links = {link for link in links if link in page_names}
    items = {
        "summary" : summary[:300] + "...",
        "URL": unquote(url),
        "links": [f"[[{link}]]" for link in links],
        "Date of visit": "[[" + ldvs[name] + "]]"
    }
    with open(file_name, "w") as write:
        write.write(yaml.dump(items, allow_unicode=True))

pbar = tqdm(page_names.items(), desc="Starting...")
for name, url in pbar:
    try:
        pbar.set_description(name)
        create_md_page(name, langs[name])
    except ReadTimeout:
        print("Timed out on ", name)
        continue
    









