from openai import OpenAI
import re
from tqdm import tqdm
from util import create_md_table, load_processed_conferences

client = OpenAI()
README_PATH = "README.md"
PROMPT_TEMPLATE = "miner/prompt_template.txt"


def load_prompt_template(file_path: str) -> str:
    with open(file_path, "r", encoding="utf8") as infile:
        return infile.read()


def apply_prompt_template(template: str, url: str) -> str:
    return template.replace("<url>", url)


def extract_url_from_markdown(md_link: str) -> str:
    if md_link.startswith("[link](") and md_link.endswith(")"):
        return md_link[7:-1]
    return ""


def update_j1c2_details_for(api: OpenAI, confs: list) -> list:
    prompt_template = load_prompt_template(PROMPT_TEMPLATE)
    for conf in tqdm(confs):
        if conf["j1c2_url"] != "":
            url = extract_url_from_markdown(conf["j1c2_url"])
            prompt = apply_prompt_template(prompt_template, url)
            # todo: error handling
            response = api.responses.create(
                model="gpt-4.1",
                input=prompt,)
            conf["partnered_journals"] = response.output[0].content[0].text
            print(conf["partnered_journals"])
    return confs


def merge_j1c2_details(original: list, updates: list) -> list:
    url_to_update = {u["url"]: u for u in updates}
    merged = []
    for conf in original:
        if conf["url"] in url_to_update:
            updated_conf = url_to_update[conf["url"]]
            conf["partnered_journals"] = updated_conf["partnered_journals"]
        merged.append(conf)
    return merged


confs = load_processed_conferences(README_PATH)

# filter for all conferences that have J1C2 but no partnered journals
confs_to_check = [c for c in confs if (c["has_j1c2"]
                  == "✅" and c["partnered_journals"] == "")]

updated_confs = update_j1c2_details_for(client, confs_to_check)

confs_merged = merge_j1c2_details(confs, updated_confs)

md_table = create_md_table(confs_merged)
readme_contens = ""
with open(README_PATH, "r", encoding="utf8") as infile:
    readme_contens = infile.read()

pattern = r"(?<=<!-- gen_start -->).*?(?=<!-- gen_end -->)"

new_text = re.sub(pattern, md_table, readme_contens, flags=re.DOTALL)

with open(README_PATH, "w", encoding="utf8") as outfile:
    outfile.write(new_text)
