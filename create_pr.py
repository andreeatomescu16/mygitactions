import os
import subprocess
import time
from github import Github
from dotenv import load_dotenv

# Încarcă variabilele de mediu din fișierul .env
load_dotenv()

# Obține variabilele de mediu
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPOSITORY')

if not GITHUB_TOKEN or not REPO_NAME:
    raise ValueError("Lipsesc variabilele de mediu GITHUB_TOKEN sau GITHUB_REPOSITORY")

# Inițializează clientul GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

def get_last_two_commits(branch):
    # Obține hash-urile ultimelor două commit-uri
    log = subprocess.check_output(['git', 'log', '--format=%H', branch, '-n', '2']).decode().split()
    return log[0], log[1]

def create_pull_request():
    branch = repo.default_branch

    # Obține ultimele două commit-uri pe branch-ul principal
    last_commit, second_last_commit = get_last_two_commits(branch)

    # Creează un branch temporar de la penultimul commit
    temp_branch_name = f'temp-pr-{int(time.time())}'
    subprocess.run(['git', 'checkout', '-b', temp_branch_name, second_last_commit])

    # Push branch-ul temporar
    subprocess.run(['git', 'push', 'origin', temp_branch_name])

    # Creează un pull request
    pr_title = 'Automatizare PR pentru ultimul commit'
    pr_body = 'Acest pull request este creat automat pentru ultimul commit.'
    repo.create_pull(title=pr_title, body=pr_body, head=branch, base=temp_branch_name)

if __name__ == "__main__":
    create_pull_request()
