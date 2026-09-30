print("Welcome to Job Track Application")

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

tracker.show_jobs()

    