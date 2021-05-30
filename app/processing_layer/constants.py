##################### GIT API #####################
ORG_REPO_URL = "https://api.github.com/orgs/{org_name}/repos"
REPO_CONTENT_URL = "https://api.github.com/repos/{owner}/{repo_name}/contents/.circleci/config.yml"


##################### CONSTANTS #####################
GIT_COMMIT_MESSAGE = "updated by yara app"
GIT_DELETE_COMMIT_MESSAGE = "all steps deleted by yara app"
REPO_COMPLAINT = "complaint"
REPO_NON_COMPLAINT = "non-complaint"
CIRCLECI_MANDATORY_STEPS = ['save_cache', 'restore_cache', 'unit-test']


