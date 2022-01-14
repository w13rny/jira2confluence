import re
import time

from atlassian import Confluence
from atlassian import Jira

import config as cfg
from models.page import Page


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


if __name__ == '__main__':
    jira = Jira(
        url=cfg.jira['url'],
        username=cfg.jira['username'],
        password=cfg.jira['api_token'],
        cloud=True
    )

    confluence = Confluence(
        url=cfg.confluence['url'],
        username=cfg.confluence['username'],
        password=cfg.confluence['api_token'],
        cloud=True
    )

    for page in cfg.pages:
        jira_page = Page(jira.jql(page['jql_request']))
        confluence.update_page(
            page_id=page['page_id'],
            title=page['page_title'],
            body=jira_page.body,
            type='page',
            representation='wiki',
            minor_edit=False
        )
        print(page['page_title'] + ' - strona została zaktualizowana.')

    # when script process only one Confluence page, 2 quick requests to update the same page causes the conflict error
    # this sleep is for avoiding the issue
    time.sleep(1)

    for page in cfg.pages:
        page_obj = confluence.get_page_by_id(page['page_id'], expand='body.storage')
        new_body = page_obj['body']['storage']['value']
        new_body = fix_newlines(new_body)
        new_body = jira_links_to_macros(new_body)
        confluence.update_page(
            page_id=page['page_id'],
            title=page['page_title'],
            body=new_body,
            type='page',
            representation='storage',
            minor_edit=False
        )
        print(page['page_title'] + ' - strona została skorygowana (znaki nowej linii i makra linków do Jiry).')
