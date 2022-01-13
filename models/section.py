import config as cfg


def keep_brackets(string: str) -> str:
    result_string = string
    result_string = result_string.replace('[', '\[')
    result_string = result_string.replace(']', '\]')
    return result_string


class Section:
    issue_key = ''
    summary = ''
    description = ''

    def __init__(self, issue):
        self.issue_key = issue['key']
        self.summary = 'h1. ' + keep_brackets(issue['fields']['summary'])
        if issue['fields']['description']:
            self.description = issue['fields']['description']
        else:
            self.description = ''

    @property
    def issue_url(self) -> str:
        return cfg.jira['issue_url_prefix'] + self.issue_key
