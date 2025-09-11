class Conference:
    def __init__(self, name: str, url: str, j1c2_url: str = "", journal_requirements: str = ""):
        self.name = name
        self.url = url
        self.j1c2_url = j1c2_url
        self.journal_requirements = journal_requirements

    @property
    def has_j1c2(self) -> bool:
        return self.j1c2_url != ""

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url,
            "j1c2_url": self.j1c2_url,
            "requirements": self.requirements
        }

    def to_markdown_row(self):
        has_j1c2 = "✅" if self.has_j1c2 else "❌"
        j1c2_link = f"[link]({self.j1c2_url})" if self.has_j1c2 else ""
        journals = self.journal_requirements if self.journal_requirements else ""
        return f"| {self.name} | [&#127968;]({self.url}) | {has_j1c2} | {j1c2_link} | {journals} |\n"

    @staticmethod
    def markdown_header():
        return "| Conference | Url | J1C2?| J1C2 Link| Journal Requirements |\n"

    def markdown_separator():
        return "|---|---|---|---|---|\n"

    @staticmethod
    def from_dict(data: dict):
        return Conference(
            name=data.get("name", ""),
            url=data.get("url", ""),
            j1c2_url=data.get("j1c2_url", ""),
            journal_requirements=data.get("journal_requirements", "")
        )

    @staticmethod
    def from_markdown_line(line: str):
        parts = line.split("|")
        if len(parts) > 2:
            conf_name = parts[1].strip()
            if conf_name:
                return Conference(
                    name=conf_name or "",
                    url=_extract_url_from_markdown(parts[2].strip()) or "",
                    j1c2_url=_extract_url_from_markdown(
                        parts[4].strip()) or "",
                    journal_requirements=parts[5].strip() or ""
                )
        return None


def _extract_url_from_markdown(md_link: str) -> str:
    supported_links = ["[&#127968;](", "[link]("]

    for link in supported_links:
        if md_link.startswith(link) and md_link.endswith(")"):
            return md_link[len(link):-1]
    return ""
