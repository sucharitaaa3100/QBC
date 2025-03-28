from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
import json
from . import db
from .models import Subject, Chapter, Quiz, Question
from .decorators import admin_required

views = Blueprint("views", __name__)

@views.route("/", methods=["GET"])
def landing_page():
    return render_template("landing_page.html", user=current_user)

@views.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for("views.admin_dashboard"))
    return render_template("user_dashboard.html")

@views.route("/about")
def about():
    return render_template("about.html")  # Ensure about.html exists

@views.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    subjects = Subject.query.all()
    return render_template("admin_dashboard.html", subjects=subjects)

@views.route("/delete_subject/<int:subject_id>", methods=["POST"])
@login_required
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash("Subject deleted successfully.", "success")
    return redirect(url_for("views.admin_dashboard"))

@views.route("/delete_chapter/<int:chapter_id>", methods=["POST"])
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

        # Check for case-insensitive duplicate
        if Subject.query.filter(db.func.lower(Subject.name) == name).first():
            flash("Subject already exists!", "error")
        else:
            new_subject = Subject(name=name, description=description)
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

@views.route("/quiz/<int:quiz_id>", methods=["GET", "POST"])
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

@views.route("/delete_quiz/<int:quiz_id>", methods=["POST"])
@login_required
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter_id = quiz.chapter_id  # Store chapter ID before deleting
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz deleted successfully.", "success")
    return redirect(url_for("views.view_quizzes", chapter_id=chapter_id))

@views.route("/edit_question/<int:quiz_id>/<int:question_id>", methods=["GET", "POST"])
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

@views.route("/delete_question/<int:question_id>", methods=["POST"])
@login_required
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id  # Store quiz ID before deleting
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted successfully!", "danger")
    return redirect(url_for("views.view_quiz", quiz_id=quiz_id))
