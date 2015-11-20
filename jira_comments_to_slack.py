from jira.client import JIRA
from time import sleep
import sys
import subprocess

#TODO: Pass credentials as args
#auth = tuple(sys.argv[1:2])

#YOU MUST ADD CREDENTIALS AS OF NOW
jira = JIRA(server='http://jira.yourserver.com:8080', basic_auth=('USERNAME','PASSWORD'))

projects = ["PUT PROJECTS","HERE"]

def get_comments():
    comments = {}
    for proj_name in projects:
        proj_arg = 'project=' + proj_name
        issues = jira.search_issues(proj_arg)
        for issue in issues:
            comments[issue.key] = jira.comments(issue.key) 
    return comments

def compare_comments(old_com,new_com):
    for issue_id, comments in new_com.items():
        if issue_id in old_com:
            for comment in comments:
                if comment.id not in map(lambda x: x.id, old_com[issue_id]):
                    slack_webhook(issue_id,comment)
        else:
            for comment in comments:
                slack_webhook(issue_id,comment)

def slack_webhook(issue_id, z):
    #TODO: Get the webhook url
    data_curl = issue_id + "\n" + "http://jira.yourserver.com:8080/browse/" + issue_id + "\n" + str(z.author) + "\n" +  str(z.body)
    #Change the token up yo
    bashCommand = "curl --data \"" + data_curl + "\" $\'https://yourslack.slack.com/services/hooks/slackbot?token=saotehusatoehusatoheusth&channel=%23your_channel\'"
    subprocess.call(bashCommand,shell=True)
    
old_comments = get_comments()
while True:
    new_comments = get_comments()
    compare_comments(old_comments,new_comments)
    old_comments = new_comments
