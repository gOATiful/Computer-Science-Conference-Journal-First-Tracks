from requests_html import HTMLSession
from tqdm import tqdm
import re


# just a quick script to mime the data from conf.researchr.org. Most definitely subject to change!

base_url = "https://conf.researchr.org/"

outfile_path = "README.md"

session = HTMLSession()
r = session.get(base_url)

r.html.render()

selected = r.html.find(
    "#content > div.row > div:nth-child(1) > div > table > tbody > tr")
samples = []

for conf in selected:
    name = conf.find("td > h3 > a")
    name = name[0].full_text
    url = conf.attrs["href"]
    sample = {"name": name,
              "url": url,
              "j1c2_url": "",
              "partnered_journals": []}
    samples.append(sample)

for s in tqdm(samples):
    r = session.get(s["url"])
    r.html.render()
    links = r.html.find("a")  # find all links
    for link in links:
        linktext = link.full_text.lower()
        if ("journal" in linktext and "first" in linktext) or "j1c2" in linktext:
            s["j1c2_url"] = link.attrs["href"]

def create_md_table(samples: list):
    header = "|Conference | Url | J1C2?| J1C2 Link| Partnered Journals|\n" + \
        "|---|---|---|---|---|\n"
    md_text = header
    for sample in samples:
        conf = sample["name"]
        link = sample["url"]
        j1c2_link = sample["j1c2_url"]
        has_j1c2 = "✅" if sample["j1c2_url"] != "" else "❌"
        j1c2_url = f"[link]({j1c2_link})" if sample["j1c2_url"] != "" else ""
        journals = "" if len(
            sample["partnered_journals"]) == 0 else sample["partnered_journals"]
        row = f"| {conf} | [&#127968;]({link}) | {has_j1c2} | {j1c2_url} | {journals} |\n"
        md_text += row
    return f"\n{md_text}\n"

md_table = create_md_table(samples)
readme_contens = ""
with open(outfile_path, "r") as infile:
    readme_contens = infile.read()

pattern = r"(?<=<!-- gen_start -->).*?(?=<!-- gen_end -->)"

new_text = re.sub(pattern, md_table, readme_contens, flags=re.DOTALL)

with open(outfile_path, "w") as outfile:
    outfile.write(new_text)
