from models.section import Section
from datetime import datetime


class Page:
    sections = []

    def __init__(self, issues):
        self.sections = []
        for issue in issues['issues']:
            self.sections.append(Section(issue))

    @property
    def table_of_content(self) -> str:
        return '{toc}'

    @property
    def separator(self) -> str:
        return '\n----\n'

    @property
    def footer(self) -> str:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        msg = '\n{color:grey}Ta strona została wygenerowana automatycznie ' + now + '.{color}'
        return msg

    @property
    def body(self) -> str:
        page_content = [self.table_of_content]
        if self.sections:
            for section in self.sections:
                page_content.append(section.summary)
                page_content.append(section.issue_url)
                page_content.append(section.description)
                page_content.append(self.separator)
        page_content.append(self.footer)
        body = '\n'.join(page_content)
        return body
