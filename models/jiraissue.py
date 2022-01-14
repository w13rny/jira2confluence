import re

import config as cfg


def keep_brackets(string: str) -> str:
    result_string = string
    result_string = result_string.replace('[', '\[')
    result_string = result_string.replace(']', '\]')
    return result_string


class JiraIssue:
    issue_key = ''
    summary = ''
    description = ''
    attachments = None

    def __init__(self, issue: dict):
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
        return cfg.jira['url'] + '/browse/' + self.issue_key

    @property
    def description_with_img_urls(self) -> str:
        desc = self.description
        if self.attachments:
            for attachment in self.attachments:
                desc = desc.replace(attachment['filename'], attachment['content'])
            img_properties = f"|width={cfg.confluence['img_width']},height={cfg.confluence['img_height']}!"
            desc = re.sub(r'(\|width\=\d{1,4},height\=\d{1,4}!)', img_properties, desc)
        return desc
