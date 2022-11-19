import datetime
from jobportal import db

class Applicants(db.Document):
    #id = db.IntField(min_value=1)
    username = db.StringField(unique=True, required=True)
    password = db.StringField(required=True)
    fname = db.StringField(required=True)
    lname = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    phone = db.StringField(required=True, unique=True)
    experience = db.StringField()
    skillset = db.StringField()
    jobsApplied = db.ListField()

    def as_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'First Name': self.fname,
            'Last Name': self.lname,
            'email': self.email,
            'phone': self.phone,
            'experience': self.experience,
            'skillset': self.skillset,
            'jobsApplied': self.jobsApplied
        }
    
    def applyJob(self, jobId):
        appliedJobs = [job["jobId"] for job in self.jobsApplied]
        if jobId in appliedJobs:
            return False
        self.jobsApplied.append(
            {
                "jobId":jobId,
                "Status":"Applied",
                "Applied on": datetime.datetime.now()
            }
        )
        self.save()
        return True
    
    def hire(self, jobId, jobTitle):
        emp = Employees(
            employeeId=Jobs.objects.count() + 1, # Auto increment jobid
            username=self.username,
            password=self.password,
            fname=self.fname,
            lname=self.lname,
            email=self.email,
            phone=self.phone,
            skillset=self.skillset,
            jobTitle=jobTitle
        ).save()
        Jobs.objects(jobId=jobId).get().closeReq(self.username)
        for job in self.jobsApplied:
            if job['jobId'] != jobId:
                Jobs.objects(jobId=jobId).get().removeApplicant(self.username)
        self.delete()

    def expireJob(self, jobId):
        for job in self.jobsApplied:
            if job["jobId"] == jobId:
                self.jobsApplied.remove(job)
                break

class Jobs(db.Document):
    jobId = db.IntField(unique=True, min_value=1, required=True)
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    experience = db.StringField(required=True)
    skills = db.StringField(required=True)
    applicants = db.ListField()

    def as_dict(self):
        return {
            'jobId': self.jobId,
            'Job Title': self.title,
            'description': self.description,
            'experience': self.experience,
            'skills': self.skills,
        }
    
    def addApplicant(self, userid):
        """ Add applicant to the job if the user hasn't applied."""
        if userid not in self.applicants:
            self.applicants.append(userid)
            self.save()
    
    def getApplicants(self):
        return self.applicants
    
    def closeReq(self, username):
        for applicant in self.applicants:
            if applicant != username:
                Applicants.objects(username=applicant).get().expireJob(self.jobId)
        self.delete()
    
    def removeApplicant(self, username):
        if username in self.applicants:
            self.applicants.remove(username)




class Employees(db.Document):
    employeeId = db.IntField(unique=True, min_value=1, required=True)
    username = db.StringField(unique=True, required=True)
    password = db.StringField(required=True)
    fname = db.StringField(required=True)
    lname = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    phone = db.StringField(required=True, unique=True)
    joinDate = db.DateTimeField(default=datetime.datetime.now)
    skillset = db.StringField()
    jobTitle = db.StringField()

    def as_dict(self):
        return {
            'employeeId': self.employeeId,
            'username': self.username,
            'password': self.password,
            'First Name': self.fname,
            'Last Name': self.lname,
            'joinDate': self.joinDate,
            'skillset': self.skillset,
            'email': self.email,
            'phone': self.phone,
            'JobTitle': self.jobTitle
        }
    