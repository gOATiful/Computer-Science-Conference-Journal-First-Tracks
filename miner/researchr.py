from requests_html import HTMLSession
from tqdm import tqdm
import re

from util import create_md_table
from model import Conference


# a quick script to mime the data from conf.researchr.org. Most definitely subject to change!

base_url = "https://conf.researchr.org/"

outfile_path = "README.md"


def update_conference_list(md_table: str, outfile_path: str):
    readme_contens = ""

    with open(outfile_path, "r") as infile:
        readme_contens = infile.read()

    pattern = r"(?<=<!-- gen_start -->).*?(?=<!-- gen_end -->)"
    new_text = re.sub(pattern, md_table, readme_contens, flags=re.DOTALL)
    with open(outfile_path, "w") as outfile:
        outfile.write(new_text)


session = HTMLSession()
r = session.get(base_url)

r.html.render()

selected = r.html.find(
    "#content > div.row > div:nth-child(1) > div > table > tbody > tr")
conferences = []

for conf in selected:
    name = conf.find("td > h3 > a")
    name = name[0].full_text
    url = conf.attrs["href"]
    conf = Conference(name=name, url=url)
    conferences.append(conf)

for conf in tqdm(conferences):
    r = session.get(conf.url)
    r.html.render()
    links = r.html.find("a")  # find all links
    for link in links:
        linktext = link.full_text.lower()
        if ("journal" in linktext and "first" in linktext) or "j1c2" in linktext:
            conf.j1c2_url = link.attrs["href"]


md_table = create_md_table(conferences)
update_conference_list(md_table, outfile_path)
print("Updated conference list in README.md")