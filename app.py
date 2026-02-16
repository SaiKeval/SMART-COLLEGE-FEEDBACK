from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="smart_feedback"
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():

    db = get_db_connection()
    cursor = db.cursor()

    # Basic Details
    name = request.form.get("name") or "Anonymous"
    roll = request.form.get("roll") or "N/A"
    department = request.form.get("department") or "N/A"
    year = request.form.get("year") or "N/A"
    section = request.form.get("section") or "N/A"
    academic_year = request.form.get("academic_year") or "2025-26"

    # Subject Details
    subject = request.form.get("subject") or "N/A"
    faculty = request.form.get("faculty") or "N/A"

    # =========================
    # RATING SECTION
    # =========================

    # Teaching Effectiveness
    subject_knowledge = int(request.form.get("subject_knowledge") or 0)
    clarity = int(request.form.get("clarity_explanation") or 0)

    # Classroom Interaction
    communication = int(request.form.get("communication_skills") or 0)
    interaction = int(request.form.get("interaction_students") or 0)
    punctuality = int(request.form.get("approachability_support") or 0)

    # =========================
    # Infrastructure & Facilities  (STEP 4 ADDED)
    # =========================
    classroom_cleanliness = int(request.form.get("classroom_cleanliness") or 0)
    lab_facilities = int(request.form.get("lab_facilities") or 0)
    library_resources = int(request.form.get("library_resources") or 0)
    wifi_availability = int(request.form.get("wifi_availability") or 0)
    washroom_cleanliness = int(request.form.get("washroom_cleanliness") or 0)

    # Overall Rating (same logic)
    rating = round(
        (subject_knowledge + clarity + communication +
         interaction + punctuality) / 5
    )

    liked = request.form.get("liked") or ""
improvements = request.form.get("improvements") or ""
suggestions = request.form.get("suggestions") or ""



    # =========================
    # UPDATED INSERT QUERY (STEP 2 FIXED)
    # =========================
    query = """
        INSERT INTO feedback 
        (name, roll, department, year, section, academic_year,
         subject, faculty, subject_knowledge, clarity,
         communication, interaction, punctuality,
         classroom_cleanliness, lab_facilities, library_resources, 
         wifi_availability, washroom_cleanliness,
         comments, submitted_at, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        name, roll, department, year, section, academic_year,
        subject, faculty,
        subject_knowledge, clarity,
        communication, interaction, punctuality,
        classroom_cleanliness, lab_facilities, library_resources,
        wifi_availability, washroom_cleanliness,
        comments,
        datetime.now(),
        rating
    )

    cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close()

    return render_template("result.html",
                           name=name,
                           roll=roll,
                           subject=subject,
                           faculty=faculty,
                           rating=rating)
