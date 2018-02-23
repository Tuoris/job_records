import os
import sqlite3
from flask import Flask, jsonify, render_template, request, redirect, url_for, g

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

    if all([v is not None for v in validated_job.values()]):
        save_record(validated_job)

    return redirect(url_for('index'))


@app.route('/delete_record', methods=['POST'])
def delete_record():
    form = request.form
    record_id = form['id']
    delete_db_record(record_id)
    return ''


@app.route('/get_record', methods=['GET'])
def fetch_record():
    record_id = request.args.get('id')
    try:
        record_id = int(record_id)
    except ValueError:
        record_id = None

    if not record_id:
        return jsonify({})

    record = get_record(record_id)
    return jsonify(record)


@app.route('/edit_record', methods=['POST'])
def edit_record():
    validated_job = {}
    form = request.form

    validated_job['job_title'] = form.get('job_title')
    validated_job['company'] = form.get('company')
    validated_job['job_url'] = form.get('job_url')

    score = form.get('score')
    salary = form.get('salary')
    record_id = form.get('id')

    validated_job['score'] = validate_score(score)
    validated_job['salary'] = validate_salary(salary)
    validated_job['record_id'] = validate_id(record_id)

    if all([v is not None for v in validated_job.values()]):
        update_record(validated_job)

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


def update_record(record):
    db = get_db()
    db.execute(
        'update job_records set job_title = (?), company = (?), '
        'job_url = (?), score = (?), salary = (?) where id==(?)',
        [record['job_title'], record['company'],
            record['job_url'], record['score'], record['salary'], record['record_id']]
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


def get_record(record_id):
    db = get_db()
    cur = db.execute(
        'select * from job_records where id==(?)',
        [record_id]
    )
    records = cur.fetchall()
    db.close()
    if records:
        record = dict(records[0])
    else:
        record = {}
    return record


def delete_db_record(record_id):
    db = get_db()
    db.execute(
        'delete from job_records where id==(?)',
        [record_id]
    )
    db.commit()
    db.close()


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
        salary = 0
    return salary


def validate_id(record_id):
    try:
        record_id = int(record_id)
    except ValueError:
        record_id = None
    return record_id


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
