from flask import Blueprint

employee_api = Blueprint('employee_api',__name__)

import jobportal.resources as resources

employee_api.add_resource(resources.AllEmployees,"/employees")
employee_api.add_resource(resources.PostJob,"/job")
employee_api.add_resource(resources.EmployeeLogin,"/employee/login")
employee_api.add_resource(resources.EmployeeLogoutAccess,"/employee/logout/access")
employee_api.add_resource(resources.EmployeeLogoutRefresh,"/employee/logout/refresh")

