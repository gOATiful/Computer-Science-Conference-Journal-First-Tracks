from requests_html import HTMLSession
from tqdm import tqdm

from util import create_md_table, load_processed_conferences, update_conference_list
from model import Conference


# a quick script to mime the data from conf.researchr.org. Most definitely subject to change!

base_url = "https://conf.researchr.org/"

README_PATH = "README.md"


def filter_existing(online: list[Conference], existing: list[Conference]) -> list[Conference]:
    existing_urls = {e.url for e in existing}
    return [o for o in online if o.url not in existing_urls]


def merge_conference_lists(original: list[Conference], updates: list[Conference]) -> list[Conference]:
    url_to_update = {u.url: u for u in updates}
    merged = []
    for conf in original:
        if conf.url in url_to_update:
            updated_conf = url_to_update[conf.url]
            conf.j1c2_url = updated_conf.j1c2_url
            conf.journal_requirements = updated_conf.journal_requirements
        merged.append(conf)
    return merged


session = HTMLSession()
r = session.get(base_url)

r.html.render()

selected = r.html.find(
    "#content > div.row > div:nth-child(1) > div > table > tbody > tr")


processed_conferences = load_processed_conferences(README_PATH)

online_conferences = []

for conf in selected:
    name = conf.find("td > h3 > a")
    name = name[0].full_text
    url = conf.attrs["href"]
    conf = Conference(name=name, url=url)
    online_conferences.append(conf)

print(f"Found {len(online_conferences)} conferences online.")

new_conferences = filter_existing(online_conferences, processed_conferences)
print(f"Found {len(new_conferences)} new conferences.")


for conf in tqdm(new_conferences):
    r = session.get(conf.url)
    r.html.render()
    links = r.html.find("a")  # find all links
    # look for J1C2 links
    for link in links:
        linktext = link.full_text.lower()
        if ("journal" in linktext and "first" in linktext) or "j1c2" in linktext:
            conf.j1c2_url = link.attrs["href"]


updated_conferences = merge_conference_lists(
    processed_conferences, new_conferences)

md_table = create_md_table(updated_conferences)
update_conference_list(md_table, README_PATH)
print(f"Updated conference list in {README_PATH}")
