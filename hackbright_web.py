"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route('/')
def list_all_projects_and_students():
    """List all projects and students"""

    records = hackbright.get_all_projects_and_students()

    return render_template('homepage.html', records=records)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

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

    return redirect('/success?github={}'.format(github))


@app.route('/success')
def confirms_student_added():

    github = request.args.get('github')

    # hackbright.get_student_by_github('github')

    return render_template('student_added.html',
                            github=github)


@app.route('/project')
def get_project_info():
    """lists title, description, and maximum grade of a project"""

    title = request.args.get('title')

    github_and_grades = hackbright.get_grades_by_title(title)

    project_record = hackbright.get_project_by_title(title)
    description = project_record[1]
    max_grade = project_record[2]

    return render_template('project_info.html',
                            title=title,
                            description=description,
                            max_grade=max_grade,
                            github_and_grades=github_and_grades)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
