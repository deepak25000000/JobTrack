from flask import Flask, request, jsonify #importing flask application class, request allows us to read the data sent to the client
app = Flask(__name__) # This creates our Flask application. Jsonify helps us to return the results properly in json

jobs = [
    {
        "id": 1,
        "role": "Software Engineer",
        "location": "Bangalore",
        "company": "Google",
        "status": "Applied"
    },
    {
        "id": 2,
        "role": "SDE Intern",
        "location": "Hyderabad",
        "company": "Microsoft",
        "status": "Rejected"
    },
    {
        "id": 3,
        "role": "SDE",
        "location": "Pune",
        "company": "Amazon",
        "status": "In-process"
    }
]
@app.route("/")
def home():
    return "Welcome to JobTrack API!"

@app.route("/api/jobs", methods=["GET"]) #this route for getting all jobs 
def get_jobs():
    return jsonify(jobs)

@app.route("/api/jobs/<int:job_id>") #When someone requests /, execute the function below.
def get_jobs_by_id(job_id): # this route for getting job for a particular id 
    for job in jobs:
        if job["id"] == job_id:
            return jsonify(job)
    return jsonify({
        "error": "Job not found"
    }), 404 #404 for not found in the data
   
@app.route("/api/jobs", methods=["POST"])
def create_job():
    data = request.json
    new_job ={
        "id": len(jobs) + 1,
        "role": data["role"],
        "location": data["location"],
        "company": data["company"],
        "status": data["status"]
    }
    jobs.append(new_job)
    return jsonify(new_job), 201 #201 is for creation and it shows the new job created 

@app.route("/api/jobs/<int:job_id>", methods=["PUT"]) #Update 
def update_job(job_id):
    data = request.json

    for job in jobs:
        if job["id"] == job_id:
            job["role"] = data["role"]
            job["location"] = data["location"]
            job["company"] = data["company"]
            job["status"] = data["status"]

            return jsonify(job)
    return jsonify({
        "error": "Job not found"
    }), 404

@app.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):

    for job in jobs:

        if job["id"] == job_id:

            jobs.remove(job)

            return jsonify({
                "message": "Job deleted successfully"
            })

    return jsonify({
        "error": "Job not found"
    }), 404
    




    

if __name__ == "__main__":
    app.run(debug=True)





# pyrefly: ignore [parse-error]
'''print("Welcome to Job Track Application")

class Job:
    def __init__(self, role, location, company, status):
        self.role = role
        self.location = location
        self.company = company
        self.status = status
    def display_Job(self):
        print(f"{self.role} at {self.company}")
        print(f"Location: {self.location}")
        print(f"Status: {self.status}")

    def update_status(self, new_status):
        self.status = new_status

class jobtracker:
    def __init__(self):
        self.jobs = []
    def add_jobs(self, jobs):
        self.jobs.append(jobs)
    def show_jobs(self):
        for job in self.jobs:
            job.display_Job()
            print()

tracker = jobtracker()


        


job1 = Job("Software Engineer", "Banglore", "Google", "Applied")
job2 = Job("SDE Intern", "Hyderabad", "Microsoft", "Rejected")
job3 = Job("SDE", "Pune", "Amazon", "In-process")

tracker.add_jobs(job1)
tracker.add_jobs(job2)
tracker.add_jobs(job3)

tracker.show_jobs() '''

    