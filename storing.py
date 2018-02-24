import sqlite3


def save_record(record, app):
    db = get_db(app)
    db.execute(
        'insert into job_records (job_title, company, job_url, score, salary) values (?, ?, ?, ?, ?)',
        [record['job_title'], record['company'],
            record['job_url'], record['score'], record['salary']]
    )
    db.commit()
    db.close()


def update_record(record, app):
    db = get_db(app)
    db.execute(
        'update job_records set job_title = (?), company = (?), '
        'job_url = (?), score = (?), salary = (?) where id==(?)',
        [record['job_title'], record['company'],
            record['job_url'], record['score'], record['salary'], record['record_id']]
    )
    db.commit()
    db.close()


def get_all_records(app):
    db = get_db(app)
    cur = db.execute(
        'select * from job_records'
    )
    records = cur.fetchall()
    db.close()
    records = [dict(r) for r in records]
    return records


def get_record(record_id, app):
    db = get_db(app)
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


def delete_record(record_id, app):
    db = get_db(app)
    db.execute(
        'delete from job_records where id==(?)',
        [record_id]
    )
    db.commit()
    db.close()


def connect_db(app):
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db(app):
    return connect_db(app)


def init_db(app):
    db = get_db(app)
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
