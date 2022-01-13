from models.issuedata import IssueData
from datetime import datetime


class Page:
    issues = []

    def __init__(self, issues):
        self.issues = []
        for issue in issues['issues']:
            self.issues.append(IssueData(issue))

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
        if self.issues:
            for issue in self.issues:
                page_content.append(issue.summary)
                page_content.append(issue.issue_url)
                page_content.append(issue.description_with_img_urls)
                page_content.append(self.separator)
        page_content.append(self.footer)
        body = '\n'.join(page_content)
        return body
