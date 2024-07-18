import os
from github import Github
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")

if not GITHUB_TOKEN or not REPO_NAME:
    raise ValueError("Missing GITHUB_TOKEN or GITHUB_REPOSITORY environment variable")

# Initialize GitHub client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

def get_latest_commit_branch():
    default_branch = repo.default_branch
    commits = repo.get_commits(sha=default_branch)
    latest_commit = commits[0]
    latest_commit_sha = latest_commit.sha

    branches = repo.get_branches()
    for branch in branches:
        branch_commits = repo.get_commits(sha=branch.name)
        if any(commit.sha == latest_commit_sha for commit in branch_commits):
            return branch.name
    return None

def create_pull_request():
    base = repo.default_branch
    head = get_latest_commit_branch()

    if head is None:
        raise ValueError("No branch found for the latest commit.")

    if head == base:
        print(f"No new changes to merge. Both head and base are {base}.")
        return

    # Create a pull request
    pr_title = f"Automated PR from {head} to {base}"
    pr_body = "This pull request is automatically created."
    pr = repo.create_pull(title=pr_title, body=pr_body, head=head, base=base)
    print(f"Pull request created: {pr.html_url}")

if __name__ == "__main__":
    create_pull_request()
