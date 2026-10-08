from flask import Blueprint, request, jsonify
from extensions import db
from models import Job
from flask_jwt_extended import jwt_required, get_jwt_identity


job_bp = Blueprint("job_bp", __name__, url_prefix="/api/jobs") #this creates a group of routes. it means evry route start with /api/jobs

@job_bp.route("", methods=["GET"]) #get method 
@jwt_required()
def get_all_jobs():
    # Get query parameters from the URL we can also apply multiple filters for the query parameter
    status = request.args.get("status") #Qurey paramter is used to pass queries in the endpoints 
    company = request.args.get("company")
    location = request.args.get("location")
    search = request.args.get("search")

    #Pagination and its parameters
    page = request.args.get("page", default=1, type=int) #this is for getting the page number.
    limit = request.args.get("limit", default=10, type=int) #this is for getting the limit.
    
    sort = request.args.get("sort", default="id") #this is for sorting the jobsacc to the required field
    order = request.args.get("order", default="asc") #this is for sorting in ascending or descending order
        
    #Validating the page
    if page < 1:
        return jsonify({
            "error": "Page number must be at least 1 or greater than 1"
        }), 400
    
    if limit < 1 or limit > 100:
        return jsonify({
            "error": "Limit must be between 1 and 100"
        }), 400
    
    user_id = get_jwt_identity()
    query = Job.query.filter_by(
    user_id=int(user_id)
    )

    # Start with all jobs from the database
    #query = Job.query

    # Filter by status if provided
    if status:
        query = query.filter_by(status=status)

    # Filter by company if provided
    if company:
        query = query.filter_by(company=company)

    # Filter by location if provided
    if location:
        query = query.filter_by(location=location)
    # Search inside the role field
    if search:
        query = query.filter(
            Job.role.ilike(f"%{search}%") #We used % and % to search for the substring in the role field. 
        ) #here python or python deveoper will match regardless of that they have written python or python deveoper in the frontend.
    
    allowed_sort_fields = {
        "id": Job.id,
        "role": Job.role,
        "company": Job.company,  #This means the client can only sort using fields we explicitly allow.
        "location": Job.location,
        "status": Job.status
    } # we did this so that the user is not able to sort using id or something


    if sort not in allowed_sort_fields:
        return jsonify({
            "error": "Invalid sort field"
        }), 400

    if order not in ["asc", "desc"]:
        return jsonify({
            "error": "Order must be asc or desc"
        }), 400

    sort_column = allowed_sort_fields[sort]

    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())


    offset = (page - 1) * limit
    jobs = query.offset(offset).limit(limit).all()

    result = []

    for current_job in jobs:
        result.append({
            "id": current_job.id,
            "role": current_job.role,
            "location": current_job.location,
            "company": current_job.company,
            "status": current_job.status,
            "user_id": current_job.user_id
        })

    return jsonify(result)

@job_bp.route("/<int:job_id>", methods=["GET"])
@jwt_required() #now these endpoints GET requieres a valid JWT 
def get_job_by_id(job_id):

    #Ask the database for the job matching the ID from the URL
    #found_job = db.session.get(Job, job_id)
    user_id = get_jwt_identity()
    found_job = Job.query.filter_by(
        id = job_id,
        user_id = int(user_id)
    ).first()

    #If the database returns nothing, send a 404 error
    if found_job is None:
        return jsonify({
            "error": "Job not found"
        }), 404

    # If it was found, return the job data
    return jsonify({
        "id": found_job.id,
        "role": found_job.role,
        "location": found_job.location,
        "company": found_job.company,
        "status": found_job.status
    })

@job_bp.route("", methods=["POST"]) #POST METHOD
@jwt_required() #here an unauthenticatd user cannot create the jobs 
def create_job():

    data = request.get_json()

    #Check whether JSON data was provided
    if data is None:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    required_fields = [
        "role",
        "location",
        "company",
        "status"
    ]

    missing_fields = []

    for field in required_fields:
        if field not in data:
            missing_fields.append(field)

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400
    
    user_id = get_jwt_identity()
    new_job = Job( 
        role=data["role"], # type: ignore
        location=data["location"], # type: ignore
        company=data["company"], # type: ignore
        status=data["status"], # type: ignore
        user_id=int(user_id) #type: ignore
    )
    db.session.add(new_job)
    db.session.commit()

    return jsonify({
        "id": new_job.id,
        "role": new_job.role,
        "location": new_job.location,
        "company": new_job.company,
        "status": new_job.status,
        "user_id":new_job.user_id
    }), 201

@job_bp.route("/<int:job_id>", methods=["PUT"]) #put method
@jwt_required()
def update_job(job_id):

    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    #found_job = db.session.get(Job, job_id)
    user_id = get_jwt_identity() #this is used for autorizaton of the user for his job only 
    found_job = Job.query.filter_by(  
        id = job_id,
        user_id = int(user_id)
    ).first()


    if found_job is None:
        return jsonify({
            "error": "Job not found"
        }), 404

    required_fields = [
        "role",
        "location",
        "company",
        "status"
    ]

    missing_fields = []

    for field in required_fields:
        if field not in data:
            missing_fields.append(field)

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    empty_fields = []

    for field in required_fields:
        if not str(data[field]).strip():
            empty_fields.append(field)

    if empty_fields:
        return jsonify({
            "error": "Fields cannot be empty",
            "fields": empty_fields
        }), 400

    allowed_statuses = [
        "Applied",
        "Interview",
        "Rejected",
        "In-process",
        "Selected"
    ]

    if data["status"] not in allowed_statuses:
        return jsonify({
            "error": "Invalid status",
            "allowed_statuses": allowed_statuses
        }), 400

    found_job.role = data["role"]
    found_job.location = data["location"]
    found_job.company = data["company"]
    found_job.status = data["status"]

    db.session.commit()

    return jsonify({
        "id": found_job.id,
        "role": found_job.role,
        "location": found_job.location,
        "company": found_job.company,
        "status": found_job.status
    })

@job_bp.route("/<int:job_id>", methods=["DELETE"])#Delete Method
@jwt_required()
def delete_job(job_id):

    #found_job = db.session.get(Job, job_id)
    user_id = get_jwt_identity() #this is used for autorizaton of the user for his job only 
    found_job = Job.query.filter_by(  #this is used for autorizaton of the user for his job only 
        id = job_id,
        user_id = int(user_id)
    ).first()

    if found_job is None:
        return jsonify({
            "error": "Job not found"
        }), 404

    db.session.delete(found_job)
    db.session.commit()

    return jsonify({
        "message": "Job deleted successfully"
    })


  