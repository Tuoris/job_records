import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'records.db'),
    SECRET_KEY='dev_key',
    USERNAME='admin',
    PASSWORD='default'
))


@app.route('/')
def index():
    records = get_records()
    return render_template('index.html', job_list=records)


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
        save_record(validated_job)

    return redirect(url_for('index'))


def save_record(record):
    db = get_db()
    db.execute(
        'insert into job_records (job_title, company, job_url, score, salary) values (?, ?, ?, ?, ?)',
        [record['job_title'], record['company'],
            record['job_url'], record['score'], record['salary']]
    )
    db.commit()
    db.close()


def get_records():
    db = get_db()
    cur = db.execute(
        'select * from job_records'
    )
    records = cur.fetchall()
    db.close()
    records = [dict(r) for r in records]
    return records


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'sqlite_db', None)
    if db is not None:
        db.close()


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


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
