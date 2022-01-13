import config as cfg


def keep_brackets(string: str) -> str:
    result_string = string
    result_string = result_string.replace('[', '\[')
    result_string = result_string.replace(']', '\]')
    return result_string


class IssueData:
    issue_key = ''
    summary = ''
    description = ''
    attachments = None

    def __init__(self, issue):
        self.issue_key = issue['key']
        self.summary = 'h1. ' + keep_brackets(issue['fields']['summary'])
        if issue['fields']['description']:
            self.description = issue['fields']['description']
        else:
            self.description = ''
        if issue['fields']['attachment']:
            self.attachments = issue['fields']['attachment']

    @property
    def issue_url(self) -> str:
        return cfg.jira['issue_url_prefix'] + self.issue_key

    @property
    def description_with_img_urls(self):
        desc = self.description
        if self.attachments:
            for attachment in self.attachments:
                desc = desc.replace(attachment['filename'], attachment['content'])
        return desc
