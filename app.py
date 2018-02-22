from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

JOB_LIST = []


@app.route('/')
def index():
    return render_template('index.html', job_list=JOB_LIST)


@app.route('/add_record', methods=['POST'])
def add_record():
    validated_job = {}
    form = request.form

    validated_job['job_title'] = form.get('job_title')
    validated_job['company'] = form.get('company')
    validated_job['job_url'] = form.get('job_url')

    score = form.get('score')
    salary = form.get('salary')

    validated_job['score'] = validate_score(score)
    validated_job['salary'] = validate_salary(salary)

    if all(validated_job.values()):
        JOB_LIST.append(validated_job)

    return redirect(url_for('index'))


def validate_score(score):
    try:
        score = int(score)
    except ValueError:
        score = None
    return score


def validate_salary(salary):
    try:
        salary = int(salary)
    except ValueError:
        salary = None
    return salary


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
