from flask import Flask, request, render_template, redirect, flash
import hackbright

app = Flask(__name__)
app.secret_key = "SHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"


@app.route("/")
def homepage():

    projects = hackbright.get_projects()
    students = hackbright.get_students()

    return render_template("homepage.html", 
                            projects=projects,
                            students=students)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)

    student_grades = hackbright.get_grades_by_github(github)
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grades=student_grades)
    return html


@app.route("/search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("search.html")


@app.route("/student-add")
def student_add():

    return render_template("/student_add.html")


@app.route("/student-added", methods=['POST'])
def handle_student_add():
    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    github = request.form.get("github")

    hackbright.make_new_student(first_name, last_name, github)

    flash("Success!")
    return redirect("/student?github={}".format(github))

@app.route("/project")
def get_project():
    """Show information about a project."""

    title = request.args.get('title', 'Markov')
    title, description, max_grade = hackbright.get_project_by_title(title)

    student_grades = {}

    for github, grade in hackbright.get_grades_by_title(title):
        full_name = hackbright.get_student_by_github(github)[0] + " " + hackbright.get_student_by_github(github)[1]
        student_grades[full_name] = [grade, github]

    html = render_template("project_info.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           grades=student_grades)
    return html

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
