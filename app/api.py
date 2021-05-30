from flask import Flask, request, Response
from flask_cors import CORS
import json
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from processing_layer import main
from db_layer import db


scheduler = BackgroundScheduler()
# uncomment below line to run scheduler for every hour
# scheduler.add_job(func=main.get_organizations, trigger="interval", minutes=60)
# uncomment below line to run scheduler for every 2 min.
scheduler.add_job(func=main.get_organizations, trigger="interval", seconds=120)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

app = Flask(__name__)
#CORS(app)


# api to get complaint report
@app.route("/yara/<org_name>/repos/complaint-status", methods=['GET'])
def get_report(org_name):
    response = main.get_repo_report(org_name)
    return json.dumps(response)


# api to get step details
@app.route("/yara/<org_name>/<repo_name>/circleci/steps", methods=['GET'])
def get_steps(org_name, repo_name):
    response = main.get_repo_steps(org_name, repo_name)
    return json.dumps(response)


# api to add step details in existing steps
@app.route("/yara/<org_name>/<repo_name>/circleci/steps", methods=['PATCH'])
def add_steps(org_name, repo_name):
    data = request.json
    response = main.add_repo_steps(org_name, repo_name, data)
    if response.status_code == 200:
        return "file updated successfully"
    else:
        return "file updation failed"


# api to delete all steps in circleci configuration
@app.route("/yara/<org_name>/<repo_name>/circleci/steps", methods=['DELETE'])
def remove_steps(org_name, repo_name):
    response = main.remove_all_steps(org_name, repo_name)
    if response.status_code == 200:
        return "all steps deleted successfully"
    else:
        return "step deletion failed"


@app.route("/yara", methods=['GET'])
def get_message():
    return "Welcome to yara"


if __name__ == '__main__':
    db.create_table()
    app.run(debug=True, host='0.0.0.0')
