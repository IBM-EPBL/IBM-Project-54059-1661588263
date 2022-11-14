import os
from flask import Flask
from flask_restful import Api
#from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine


app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'jpdb',
    #'username': 'root',
    #'password': 'root-rusteez',
    'host': os.environ['MONGO_HOST'],
    'port': int(os.environ['MONGO_PORT'])
}
#app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
db = MongoEngine()
db.init_app(app)

#mongo = PyMongo(app)

import jobportal.views as views
import jobportal.models as models 
import jobportal.resources as resources

# Applicant specific routes
api.add_resource(resources.ApplicantRegistration,"/applicant/register")
api.add_resource(resources.ApplicantLogin,"/applicant/login")
api.add_resource(resources.ApplicantLogoutAccess,"/applicant/logout/access")
api.add_resource(resources.ApplicantLogoutRefresh,"/applicant/logout/refresh")
api.add_resource(resources.ApplicationStatus,"/applicant/<userId>/<jobId>/status")
api.add_resource(resources.ApplicantJobsApplied,"/applicant/<userId>/jobs/applied")


# Job specific routes
api.add_resource(resources.JobApply,"/job/<jobId>/apply")
api.add_resource(resources.JobDetails,"/job/<jobId>")
api.add_resource(resources.PostJob,"/job")
api.add_resource(resources.AllJobs,"/jobs")
api.add_resource(resources.JobApplicants,"/job/<jobId>/applicants")
api.add_resource(resources.HireApplicant,"/job/<jobId>/hire")


# Employee specific routes
api.add_resource(resources.AllEmployees,"/employees")
api.add_resource(resources.EmployeeLogin,"/employee/login")
api.add_resource(resources.EmployeeLogoutAccess,"/employee/logout/access")
api.add_resource(resources.EmployeeLogoutRefresh,"/employee/logout/refresh")
api.add_resource(resources.AllApplicants,"/applicants")