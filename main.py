import time

from atlassian import Confluence
from atlassian import Jira

import config as cfg
from models.storagepage import StoragePage
from models.wikipage import WikiPage


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
        jira_page = WikiPage(jira.jql(page['jql_request']))
        confluence.update_page(
            page_id=page['page_id'],
            title=page['page_title'],
            body=jira_page.body,
            type='page',
            representation='wiki',
            minor_edit=False
        )
        print(page['page_title'] + ' - strona została zaktualizowana.')

    # When the script is processing only one Confluence page,
    # 2 quick requests about updating the same page causes the conflict error.
    # This sleep is for avoiding the issue.
    time.sleep(1)

    for page in cfg.pages:
        confluence_page = StoragePage(confluence.get_page_by_id(page['page_id'], expand='body.storage'))
        confluence.update_page(
            page_id=page['page_id'],
            title=page['page_title'],
            body=confluence_page.tweaked_body,
            type='page',
            representation='storage',
            minor_edit=False
        )
        print(page['page_title'] + ' - strona została skorygowana (znaki nowej linii i makra linków do Jiry).')
