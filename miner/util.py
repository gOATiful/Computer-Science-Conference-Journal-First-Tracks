from model import Conference
import re


def create_md_table(conferences: list):
    table_header = Conference.markdown_header() + \
        Conference.markdown_separator()
    table = table_header
    for conference in conferences:
        table += conference.to_markdown_row()
    return f"\n{table}\n"


def load_processed_conferences(file_path) -> list[Conference]:
    with open(file_path, "r", encoding="utf8") as infile:
        lines = infile.readlines()

    processed = []
    for line in lines:
        if line.startswith("|"):
            # skip header and separator
            if not any(x in line for x in ["Conference", "---"]):
                conf = Conference.from_markdown_line(line)
                if not conf:
                    print(f"Failed to parse line: {line}")
                else:
                    processed.append(conf)
    return processed


def update_conference_list(md_table: str, outfile_path: str):
    readme_contens = ""
    with open(outfile_path, "r") as infile:
        readme_contens = infile.read()

    pattern = r"(?<=<!-- gen_start -->).*?(?=<!-- gen_end -->)"
    new_text = re.sub(pattern, md_table, readme_contens, flags=re.DOTALL)
    with open(outfile_path, "w") as outfile:
        outfile.write(new_text)
