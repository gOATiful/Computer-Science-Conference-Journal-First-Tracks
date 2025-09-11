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


def load_processed_conferences(file_path):
    with open(file_path, "r", encoding="utf8") as infile:
        lines = infile.readlines()

    processed = []
    for line in lines:
        if line.startswith("|"):
            parts = line.split("|")
            if len(parts) > 2:
                conf_name = parts[1].strip()
                if conf_name and conf_name not in ["Conference", "---"]:
                    conf = {
                        "name": conf_name or "",
                        "url": parts[2].strip() or "",
                        "has_j1c2": parts[3].strip(),
                        "j1c2_url": parts[4].strip() or "",
                        "partnered_journals": parts[5].strip() or ""
                    }
                    processed.append(conf)
    return processed