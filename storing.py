import os
import psycopg2


DATABASE_URL = os.environ['DATABASE_URL']


def save_record(record, app):
    db = get_db(app)
    db.execute(
        'insert into job_records (job_title, company, job_url, score, salary) values (%s, %s, %s, %s, %s)',
        (record['job_title'], record['company'],
            record['job_url'], record['score'], record['salary'])
    )
    db.connection.commit()
    db.close()


def update_record(record, app):
    db = get_db(app)
    db.execute(
        'update job_records set job_title = (%s), company = (%s), '
        'job_url = (%s), score = (%s), salary = (%s) where id = %s',
        (record['job_title'], record['company'],
            record['job_url'], record['score'], record['salary'], record['record_id'])
    )
    db.connection.commit()
    db.close()


def get_all_records(app):
    db = get_db(app)
    db.execute(
        'select * from job_records'
    )
    records = db.fetchall()
    db.close()
    records = [extract(r) for r in records]
    return records


def get_record(record_id, app):
    db = get_db(app)
    db.execute(
        'select * from job_records where id = %s',
        (record_id,)
    )
    records = db.fetchall()
    db.close()
    if records:
        record = extract(records[0])
    else:
        record = {}
    return record


def delete_record(record_id, app):
    db = get_db(app)
    db.execute(
        'delete from job_records where id = %s',
        (record_id,)
    )
    db.connection.commit()
    db.close()


def extract(record):

    record_data = {
        'id': record[0],
        'job_title': record[1],
        'company': record[2],
        'job_url': record[3],
        'score': record[4],
        'salary': record[5],
    }

    return record_data


def connect_db(app):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    return cur


def get_db(app):
    return connect_db(app)


def init_db(app):
    db = get_db(app)
    with app.open_resource('schema.sql', mode='r') as f:
        db.execute(f.read())
    db.connection.commit()
