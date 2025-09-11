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

    @staticmethod
    def markdown_header():
        return "|Conference | Url | J1C2?| J1C2 Link| Journal Requirements|\n"

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
                    url=parts[2].strip() or "",
                    j1c2_url=parts[4].strip() or "",
                    journal_requirements=parts[5].strip() or ""
                )
        return Conference("", "")
