"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route('/')
def list_all_projects_and_students():
    """List all projects and students"""

    projects = hackbright.get_all_projects()

    github = hackbright.get_all_students()

    return render_template('homepage.html', github=github, projects=projects)


@app.route("/student/<github>")
def get_student(github):
    """Show information about a student."""


    first, last, github = hackbright.get_student_by_github(github)

    records = hackbright.get_grades_by_github(github)

    return render_template('student_info.html',
                           first=first,
                           last=last,
                           github=github,
                           records=records)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template('student_search.html')


@app.route("/student-add-form")
def form_to_add_student():
    """Show form for adding a new student to database."""

    return render_template('new_student.html')


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return redirect('/success/{github}'.format(github=github))


@app.route('/success/<github>')
def confirms_student_added(github):

    # github = request.args.get('github')

    return render_template('student_added.html',
                            github=github)


@app.route('/project/<title>')
def get_project_info(title):
    """lists title, description, and maximum grade of a project"""


    github_and_grades = hackbright.get_grades_by_title(title)

    title, description, max_grade = hackbright.get_project_by_title(title)

    return render_template('project_info.html',
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           github_and_grades=github_and_grades)


@app.route('/project-add-form')
def form_to_add_project():
    """Form for adding a new project to database."""

    return render_template('project_form.html')


@app.route("/add-new-project", methods=['POST'])
def project_add():
    """Add a project."""

    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.make_new_project(title, description, max_grade)

    return redirect('/project-success/{title}'.format(title=title))


@app.route('/project-success/<title>')
def confirms_project_added(title):

    # title = request.args.get('title')

    return render_template('project_added.html', title=title)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
