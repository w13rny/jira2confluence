import re
import config as cfg


def fix_newlines(body: str) -> str:
    body = body.replace('<br />\n', '\n')
    body = body.replace('\t', '')
    return body


def jira_links_to_macros(body: str) -> str:
    jira_link = cfg.jira['url'] + '/browse/'
    jira_link = jira_link.replace('/', '\/')
    regex = '(<a href="' + jira_link + '[^>]*>)(' + jira_link + ')([^<]*)(<\/a>)'
    result = re.sub(
        regex,
        f"{cfg.confluence['jira_macro_prefix']}\\3{cfg.confluence['jira_macro_suffix']}",
        body)
    return result


class StoragePage:
    body = ''

    def __init__(self, confluence_page: dict):
        self.body = confluence_page['body']['storage']['value']

    @property
    def tweaked_body(self) -> str:
        new_body = fix_newlines(self.body)
        new_body = jira_links_to_macros(new_body)
        return new_body
