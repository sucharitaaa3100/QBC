from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from sqlalchemy import func
import json
from . import db
from .models import Subject, Chapter, Quiz, Question, Score, User
from .decorators import admin_required, user_required

views = Blueprint("views", __name__)

@views.route("/", methods=["GET"])
def landing_page():
    return render_template("landing_page.html", user=current_user)

@views.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for("views.admin_dashboard"))
    return redirect(url_for("views.user_dashboard"))

@views.route("/about")
def about():
    return render_template("about.html")  # Ensure about.html exists

@views.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    subjects = Subject.query.all()
    return render_template("admin_dashboard.html", subjects=subjects)

@views.route("/admin/delete_subject/<int:subject_id>", methods=["POST"])
@login_required
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash("Subject deleted successfully.", "success")
    return redirect(url_for("views.admin_dashboard"))

@views.route("/admin/delete_chapter/<int:chapter_id>", methods=["POST"])
@login_required
@admin_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    subject_id = chapter.subject_id  # Save subject_id before deletion
    db.session.delete(chapter)
    db.session.commit()
    flash("Chapter deleted successfully.", "success")
    return redirect(url_for("views.view_chapters", subject_id=subject_id))

@views.route("/admin/add_subject", methods=["GET", "POST"])
@login_required
@admin_required
def add_subject():
    if request.method == "POST":
        name = request.form.get("name", "").strip().lower()  # Convert to lowercase
        description = request.form.get("description", "").strip()
        qualification = request.form.get("qualification", "").strip()

        # Check for case-insensitive duplicate
        if Subject.query.filter(db.func.lower(Subject.name) == name).first():
            flash("Subject already exists!", "error")
        else:
            new_subject = Subject(name=name, description=description, qualification=qualification)
            db.session.add(new_subject)
            db.session.commit()
            flash("Subject added successfully!", "success")

        return redirect(url_for("views.admin_dashboard"))

    return render_template("add_subject.html")

@views.route("/admin/chapters/<int:subject_id>")
@login_required
@admin_required
def view_chapters(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    
    return render_template("view_chapters.html", subject=subject, chapters=chapters)

@views.route("/admin/add_chapter/<int:subject_id>", methods=["GET", "POST"])
@login_required
@admin_required
def add_chapter(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    if request.method == "POST":
        name = request.form.get("name").strip()
        description = request.form.get("description").strip()

        new_chapter = Chapter(name=name, description=description, subject_id=subject.id)
        db.session.add(new_chapter)
        db.session.commit()
        flash("Chapter added successfully!", "success")
        return redirect(url_for("views.view_chapters", subject_id=subject.id))  

    return render_template("add_chapter.html", subject=subject)

@views.route("/admin/quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
@admin_required
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()

    if request.method == "POST":
        question_text = request.form.get("question_text")  # Ensure this matches the model field name
        option_a = request.form.get("option_a")
        option_b = request.form.get("option_b")
        option_c = request.form.get("option_c")
        option_d = request.form.get("option_d")
        correct_option = request.form.get("correct_option")

        new_question = Question(
            quiz_id=quiz.id,
            question_text=question_text,  # Use the correct column name
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option,
        )
        db.session.add(new_question)
        db.session.commit()
        flash("Question added successfully!", "success")
        return redirect(url_for("views.view_quiz", quiz_id=quiz.id))

    return render_template("view_quiz.html", quiz=quiz, questions=questions)

@views.route("/admin/add_quiz/<int:chapter_id>", methods=["GET", "POST"])
@login_required
@admin_required
def add_quiz(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)

    if request.method == "POST":
        try:
            time_duration = int(request.form.get("time_duration"))
            remarks = request.form.get("remarks").strip()

            new_quiz = Quiz(chapter_id=chapter.id, time_duration=time_duration, remarks=remarks)
            db.session.add(new_quiz)
            db.session.commit()
            flash("Quiz added successfully!", "success")
            return redirect(url_for("views.view_quizzes", chapter_id=chapter.id))
        except ValueError:
            flash("Time duration must be a valid number!", "error")

    return render_template("add_quiz.html", chapter=chapter)

@views.route("/admin/view_quizzes/<int:chapter_id>")
@login_required
@admin_required
def view_quizzes(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
    return render_template("view_quizzes.html", chapter=chapter, quizzes=quizzes)

@views.route("/admin/delete_quiz/<int:quiz_id>", methods=["POST"])
@login_required
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter_id = quiz.chapter_id  # Store chapter ID before deleting
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz deleted successfully.", "success")
    return redirect(url_for("views.view_quizzes", chapter_id=chapter_id))

@views.route("/admin/edit_question/<int:quiz_id>/<int:question_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_question(quiz_id, question_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    question = Question.query.get_or_404(question_id)

    if request.method == "POST":
        question.question_text = request.form["question_text"]
        question.option_a = request.form["option_a"]
        question.option_b = request.form["option_b"]
        question.option_c = request.form["option_c"]
        question.option_d = request.form["option_d"]
        question.correct_option = request.form["correct_option"]
        db.session.commit()
        flash("Question updated successfully!", "success")
        return redirect(url_for("views.view_quiz", quiz_id=quiz.id))

    return render_template("edit_question.html", quiz=quiz, question=question)

@views.route("/admin/delete_question/<int:question_id>", methods=["POST"])
@login_required
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id  # Store quiz ID before deleting
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted successfully!", "danger")
    return redirect(url_for("views.view_quiz", quiz_id=quiz_id))

@views.route("/admin/analytics")
@login_required
@admin_required
def admin_analytics():
    if not current_user.is_admin:
        return "Unauthorized", 403
    
    # Total Users
    total_users = User.query.count()
    
    # Total Quizzes
    total_quizzes = Quiz.query.count()
    
    # Total Attempts
    total_attempts = Score.query.count()
    
    # Average Score per Quiz
    avg_scores = (
        db.session.query(Quiz.id, func.avg(Score.total_score).label("avg_score"))
        .join(Score, Score.quiz_id == Quiz.id)
        .group_by(Quiz.id)
        .all()
    )
    
    avg_score_data = {quiz_id: avg_score for quiz_id, avg_score in avg_scores}
    
    return render_template("admin_analytics.html", 
                           total_users=total_users, 
                           total_quizzes=total_quizzes,
                           total_attempts=total_attempts,
                           avg_score_data=avg_score_data)

@admin_required
@login_required
@views.route('/admin/quiz/<int:quiz_id>/toggle_publish', methods=['POST'])
def toggle_publish(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    quiz.published = not quiz.published
    db.session.commit()
    return redirect(request.referrer)


@views.route("/user")
@login_required
@user_required
def user_dashboard():
    quizzes = (
        db.session.query(
            Quiz.id,
            Chapter.name.label("chapter_name"),
            Subject.name.label("subject_name"),
            db.func.count(Question.id).label("total_questions"),
            db.func.coalesce(
                db.session.query(Score.total_score)
                .filter(Score.user_id == current_user.id, Score.quiz_id == Quiz.id)
                .order_by(Score.time_stamp_of_attempt.desc())
                .limit(1)
                .scalar_subquery(),
                None
            ).label("latest_score")
        )
        .join(Chapter, Quiz.chapter_id == Chapter.id)
        .join(Subject, Chapter.subject_id == Subject.id)
        .outerjoin(Question, Question.quiz_id == Quiz.id)
        .filter(Quiz.published == True)  # Ensure only published quizzes are fetched
        .group_by(Quiz.id, Chapter.name, Subject.name)
        .all()
    )

    return render_template("user_dashboard.html", quizzes=quizzes)


@views.route("/user/quiz/<int:quiz_id>", methods=["GET"])
@login_required
@user_required
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # Check if the user has already attempted the quiz
    previous_attempt = Score.query.filter_by(user_id=current_user.id, quiz_id=quiz_id).first()
    if previous_attempt:
        flash("You have already attempted this quiz. Multiple attempts are not allowed. Ask admin - qbc_admin@fastmail.com", "warning")
        return redirect(url_for("views.user_dashboard"))

    questions = Question.query.filter_by(quiz_id=quiz.id).all()

    # Attach options to each question
    for question in questions:
        question.options = question.get_options()  # Ensure each question has an options dict

    # Flash a warning alert before quiz starts
    flash("⚠️ Before you start, ensure a stable internet connection and avoid switching tabs. Any violations may auto-submit your quiz.", "info")

    return render_template("quiz_page.html", quiz=quiz, questions=questions)




@views.route("/user/quiz/submit", methods=["POST"])
@login_required
@user_required
def submit_quiz():
    quiz_id = request.form.get("quiz_id")  # Get quiz_id from form-data

    if not quiz_id:  # Debugging issue
        return jsonify({"success": False, "message": "Error: Quiz ID is missing!"}), 400

    responses = {key.replace("question_", ""): value for key, value in request.form.items() if key.startswith("question_")}

    # Fetch relevant questions
    questions = Question.query.filter(Question.quiz_id == quiz_id, Question.id.in_(map(int, responses.keys()))).all()

    correct_answers = sum(1 for q in questions if q.correct_option.upper() == responses.get(str(q.id), "").strip().upper())

    # Store the score
    score = Score(user_id=current_user.id, quiz_id=int(quiz_id), total_score=correct_answers)
    db.session.add(score)
    db.session.commit()

    return jsonify({"success": True, "message": "Quiz submitted successfully!", "score": correct_answers})

@user_required
@views.route("/user/analytics")
@login_required
def user_analytics():
    # User's Total Quiz Attempts
    user_attempts = Score.query.filter_by(user_id=current_user.id).count()
    
    # User's Average Score
    user_avg_score = db.session.query(func.avg(Score.total_score)).filter_by(user_id=current_user.id).scalar() or 0
    
    # Score History
    score_history = (
        db.session.query(Quiz.id, Score.total_score, Score.time_stamp_of_attempt)
        .join(Quiz, Score.quiz_id == Quiz.id)
        .filter(Score.user_id == current_user.id)
        .order_by(Score.time_stamp_of_attempt)
        .all()
    )
    
    return render_template("user_analytics.html", 
                           user_attempts=user_attempts, 
                           user_avg_score=user_avg_score,
                           score_history=score_history)

