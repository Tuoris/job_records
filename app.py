import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, g
from .validation import validate_form, validate_id
from .storing import get_record, get_all_records, save_record, update_record, delete_record
from .storing import init_db
from .info_utils import m_rabota_info, work_ua_info, jobs_dou_info

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
    records = get_all_records(app)
    return render_template('index.html', job_list=records)


@app.route('/add_record', methods=['POST'])
def add_record():
    form = request.form
    valid_form = validate_form(form)

    if valid_form:
        save_record(valid_form, app)

    return redirect(url_for('index'))


@app.route('/delete_record', methods=['POST'])
def handle_delete_record():
    form = request.form
    record_id = form['id']
    delete_record(record_id, app)
    return ''


@app.route('/get_record', methods=['GET'])
def handle_get_record():
    record_id = request.args.get('id')
    try:
        record_id = int(record_id)
    except ValueError:
        record_id = None

    if not record_id:
        return jsonify({})

    record = get_record(record_id, app)
    return jsonify(record)


@app.route('/edit_record', methods=['POST'])
def handle_edit_record():
    form = request.form
    valid_id = validate_id(form.get('id'))
    valid_form = validate_form(form)
    valid_form['record_id'] = valid_id

    if valid_form and valid_id:
        update_record(valid_form, app)

    return redirect(url_for('index'))


@app.route('/get_info')
def handle_get_info():
    job_url = request.args.get('url')
    if 'm.rabota.ua' in job_url:
        info = m_rabota_info(job_url)
    elif 'www.work.ua' in job_url:
        info = work_ua_info(job_url)
    elif 'jobs.dou.ua' in job_url:
        info = jobs_dou_info(job_url)
    else:
        info = {}

    return jsonify(info)


@app.cli.command('initdb')
def initdb_command():
    init_db(app)
    print('Database initialized.')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
