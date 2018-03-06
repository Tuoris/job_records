def validate_form(form):
    valid_form = {}
    valid_form['job_title'] = form.get('job_title')
    valid_form['company'] = form.get('company')
    valid_form['job_url'] = form.get('job_url')

    score = form.get('score')
    salary = form.get('salary')
    valid_form['score'] = validate_score(score)
    valid_form['salary'] = validate_salary(salary)

    is_form_valid = all(
        [v is not None for v in valid_form.values()]
    )

    if is_form_valid:
        return valid_form
    return is_form_valid


def validate_score(score):
    try:
        score = int(score)
    except ValueError:
        return
    if score in range(1, 5+1):
        return score
    return


def validate_salary(salary):
    try:
        salary = int(salary)
    except ValueError:
        salary = 0
    if salary < 0:
        salary = 0
    return salary


def validate_id(record_id):
    try:
        record_id = int(record_id)
    except ValueError:
        record_id = None
    return record_id
