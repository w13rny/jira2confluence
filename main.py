from pprint import pprint

from atlassian import Jira

import config as cfg

if __name__ == '__main__':
    jira = Jira(
        url=cfg.jira['url'],
        username=cfg.jira['username'],
        password=cfg.jira['api_token'],
        cloud=True
    )
    issues = jira.jql(cfg.jira['jql_request'])
    pprint(issues)
