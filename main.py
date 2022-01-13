from atlassian import Confluence
from atlassian import Jira

import config as cfg
from models.page import Page

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
