from flask_restful import Resource, reqparse
from flask import jsonify
from jobportal.models import Applicants, Jobs, Employees


class ApplicantRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='Need username for registration', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        parser.add_argument('fname', help='Need first name for registration', required=True)
        parser.add_argument('lname', help='Need last name for registration', required=True)
        parser.add_argument('phone', help='Need phone number for registration', required=True)
        parser.add_argument('email', help='Need email-id for registration', required=True)
        parser.add_argument('experience', help='Experience of the applicant', required=False)
        parser.add_argument('skillset', help='skillset of the applicant', required=False)
        new_applicant = parser.parse_args()
        try:
            Applicants(
                username=new_applicant['username'],
                password=new_applicant['password'],
                fname=new_applicant['fname'],
                lname=new_applicant['lname'],
                email=new_applicant['email'],
                phone=new_applicant['phone'],
                experience=new_applicant['experience'],
                skillset=new_applicant['skillset'] 
            ).save()
        except Exception as err:
            return {'message': 'Something wrong in registration', 'exception': str(err)}
        #return data
        return {'message':'Applicant registered successfully!!!'}

class ApplicantLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        applicant = parser.parse_args()
        try:
            existing_applicant = Applicants.objects(username=applicant['username']).get().as_dict()
            pwd = existing_applicant.pop('password')
            if pwd != applicant['password']:
                return {'message': 'Invaid credentials'}
            #applicant_data = existing_applicant.to_dict()
        except Exception as err:
            return {'message': 'Error not able to find user {}'.format(applicant['username']), 'exception': str(err)}
        #return data
        return jsonify(existing_applicant)

class ApplicantLogoutAccess(Resource):
    def post(self):
        return {'message':'Applicant logged out successfully'}

class ApplicantLogoutRefresh(Resource):
    def post(self):
        return {'message': 'Applicant log out'}

class ApplicantTokenRefresh(Resource):
    def post(self):
        return {'message':'Applicant Token Refresh'}

class ApplicationStatus(Resource):
    def get(self,userId, jobId):
        return {'message':'get the status of the job application {} by {}'.format(jobId, userId)}

class ApplicantJobsApplied(Resource):
    def get(self, userId):
        return {'message': 'get all the jobs applied by {}'.format(userId)}

class EmployeeLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        return {'message':'Welcome to Employee Portal', 'user_details': data}

class EmployeeLogoutAccess(Resource):
    def post(self):
        return {'message': 'Thanks for using Employee Portal'}

class EmployeeLogoutRefresh(Resource):
    def post(self):
        return {'message': 'Employee log out'}

class EmployeeTokenRefresh(Resource):
    def post(self):
        return {'message':'Employee Token Refresh'}

class AllEmployees(Resource):
    def get(self):
        allEmp = [emp.as_dict() for emp in Employees.objects.all()]
        for empl in allEmp:
            empl.pop('password')
        return jsonify(employees = allEmp)
        #return {'message': 'List of Employees'}

    def delete(self):
        return {'message': 'Delete all employees'}

class AllApplicants(Resource):
    def get(self):
        allApplicants = [appl.as_dict() for appl in Applicants.objects.all()]
        for appl in allApplicants:
            appl.pop('password')
        return jsonify(applicants = allApplicants)

    def delete(self):
        return {'message': 'Delete all Applicants'}

class PostJob(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', help='This field cannot be blank', required=True)
        parser.add_argument('description', help='This field cannot be blank', required=True)
        parser.add_argument('skillset', help='This field cannot be blank', required=True)
        parser.add_argument('experience', help='This field cannot be blank', required=True)
        new_job = parser.parse_args()
        try:
            Jobs(
                jobId=Jobs.objects.count() + 1, # Auto increment jobid
                title=new_job['title'],
                description=new_job['description'],
                skills=new_job['skillset'],
                experience=new_job['experience']
            ).save()
        except Exception as err:
            return {'message': 'Error in posting job', 'exception': str(err)}
        return {'message': 'Posted new job to portal Successfully'}

class JobDetails(Resource):
    def get(self, jobId):
        return jsonify(Jobs.objects(jobId=jobId).get().as_dict())
        #return {'message': 'Job {} details page'.format(jobId)}

class AllJobs(Resource):
    def get(self):
        alljobs = [ job.as_dict() for job in Jobs.objects.all_fields()]
        return jsonify(jobs = alljobs)
    
    def delete(self):
        return {'message': 'Delete all Jobs posted'}

class JobApplicants(Resource):
    def get(self, jobId):
        applicants = Jobs.objects(jobId=jobId).get().getApplicants()
        return jsonify(applicants=applicants)

class JobApply(Resource):
    def post(self, jobId):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        try:
            applicant = Applicants.objects(username=data['username']).get()
            job = Jobs.objects(jobId=jobId).get()
            jobapplied = applicant.applyJob(jobId)
            if jobapplied:
                job.addApplicant(data['username'])
            else:
                return {'message':'Already applied for the job {}'.format(jobId)}
        except Exception as err:
            return {'message': 'Internal error applying for job', 'exception': str(err)}
        
        return {'message': 'Applied to the job Successfuly !!!'}

class HireApplicant(Resource):
    def post(self, jobId):
        parser = reqparse.RequestParser()
        parser.add_argument('applicant', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        try:
            applicant = Applicants.objects(username=data['applicant']).get()
            job = Jobs.objects(jobId=jobId).get()
            applicant.hire(jobId, job.title)
        except Exception as err:
            return {'message': 'Not able to hiring the applicant', 'exception': str(err)}
        
        return {'message': 'Hiring success'}
            