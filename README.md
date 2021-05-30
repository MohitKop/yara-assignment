# YARA Assignment POC

## POC Details

---

This poc will check the compliance of repositories with respect to the mandatory CircleCI steps present in the repository. A large organization works on number of projects at a time. When working with large number of repositories it is important to know they are following mandatory steps e.g. CircleCI mandatory steps. This POC automates above mentioned task.

### Features

---

- User can perform operation on CircleCI steps through API's. (More details about API operations will be found in API design document)
- User can get the concise report of repo compliance status.
- POC use scheduler which runs every 2 min. to fetch the details from Github organization.

### Requirements

---

- An AWS account.
  This poc uses dynamodb for storing the details. To create the dynamodb user must have an AWS account.
- Docker installed on machine.

### Technologies used

---

- *langauge* - Python
- *web framework* - Flask
- *database* - Dynamodb 
- *containerization tool* - Docker

#### WHY FLASK?
Flask is lightweight, micro framework, equipped with all features needed for web app designing.
#### WHY DYNAMODB?
DynamoDB is NoSQL database. The dynamic and vast variaty of steps available in CircleCI makes NoSQL more appealing than SQL.
Besides it's a fully managed service with benifits like auto-scaling, in-memory caching, backup and restore option etc.

### Get started

---

- Clone the github repo.
  > $ git clone <url>

- Create an AWS access key id and secret access key for programmatic access.

  For more details check, 

  https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html

  configure these in 'credentials' file.

  You can optionally configure the region in 'config' file. [Bydefault us-east-1]

- Create an access token for Github.

  For more details check,

  https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token#:~:text=Click%20Generate%20new%20token.,the%20command%20line%2C%20select%20repo.

  configure this token in 'github-variables.env' file.

- Add the names of organizations in 'org.yml' file.

- On local machine go to the project directory(/app folder) and use following docker command.
  > $ docker-compose up

Application will start running on port 5000, on localhost.

### Assumptions

---

- This POC deal only with repos present in Organization.
- This POC support only organization present under one account at a time.
- We have considered every repo contain '.circleci' folder and 'config.yml' file in it.
- Steps are collection of executable commands under job. Nature of steps are vary dynamic thus as of now this POC deals only steps available under jobs main build section. Considering this every config.yml should contain following block, (also check sample config file under documentation.)

        jobs:
            build: # this is main build.
                steps:
                    - step 1
                    - step 2
- We have considered following as mandatory steps,
> restore_cache, save_cache, unit-test

### What's Next?

---


We are capable to scale this app further by following ways,
- Add more API's.
- Add more steps under mandatory steps collection, against which we can check compliance.

And much more.
Also, please let me know if you want me to add/update any perticular feature. :blush:







