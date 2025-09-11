from openai import OpenAI
from tqdm import tqdm
from model import Conference
from util import create_md_table, load_processed_conferences, update_conference_list

client = OpenAI()
README_PATH = "README.md"
PROMPT_TEMPLATE = "miner/prompt_template.txt"


def load_prompt_template(file_path: str) -> str:
    with open(file_path, "r", encoding="utf8") as infile:
        return infile.read()


def apply_prompt_template(template: str, url: str) -> str:
    return template.replace("<url>", url)


def update_j1c2_details_for(api: OpenAI, confs: list[Conference]) -> list:
    prompt_template = load_prompt_template(PROMPT_TEMPLATE)
    for conf in tqdm(confs):
        if conf.j1c2_url != "":
            prompt = apply_prompt_template(prompt_template, conf.j1c2_url)
            # todo: error handling
            response = api.responses.create(
                model="gpt-4.1",
                input=prompt,)
            conf.journal_requirements = response.output[0].content[0].text
            print(conf.journal_requirements)
    return confs


def merge_j1c2_details(original: list[Conference], updates: list[Conference]) -> list[Conference]:
    url_to_update = {u.url: u for u in updates}
    merged = []
    for conf in original:
        if conf.url in url_to_update:
            updated_conf = url_to_update[conf.url]
            conf.journal_requirements = updated_conf.journal_requirements
        merged.append(conf)
    return merged


confs = load_processed_conferences(README_PATH)

# filter for all conferences that have J1C2 but no journal requirements yet
confs_to_check = [c for c in confs if (
    c.has_j1c2 and c.journal_requirements == "")]
print(f"Found {len(confs_to_check)} conferences to check for J1C2 details.")

updated_confs = update_j1c2_details_for(client, confs_to_check)

confs_merged = merge_j1c2_details(confs, updated_confs)

md_table = create_md_table(confs_merged)


update_conference_list(md_table, README_PATH)
print(f"Updated conference list in {README_PATH}")
