from flask import render_template, redirect, url_for, jsonify
from app import app, db, celery
from app.forms import SiteForm
from .models import Results, Tasks, TaskStatus
import requests
import nsq
import os
import json
# import tornado.ioloop

@celery.task
def py_counter(rec_id):
    task = Tasks.query.get(rec_id)
    task.task_status = TaskStatus.PENDING
    db.session.commit()
    resp = None
    new_result = {'address': task.address}
    try:
        resp = requests.get(task.address, timeout=10)
    except requests.exceptions.HTTPError:
        pass
    except requests.exceptions.Timeout:
        resp.status_code = 524
    except Exception:
        return
    else:
        new_result['words_count'] = resp.text.lower().count('python')
    finally:
        task.task_status = TaskStatus.FINISHED
        db.session.commit()
    new_result['http_status_code'] = resp.status_code

    # data = json.dumps(new_result)
    r = requests.post(url = f"http://{os.environ.get('HTTP_ADDRESSES')}/pub?topic={os.environ.get('TOPIC')}", json = new_result)
    # writer = nsq.Writer([os.environ.get('TCP_ADDRESSES')])
    # writer.pub(os.environ.get('TOPIC'), json.dumps(new_result))
    # nsq.run()
    print(f"put in nsq { r } {os.environ.get('HTTP_ADDRESSES')}/pub?topic={os.environ.get('TOPIC')}")

    # new_result = Results(**new_result)
    task.http_status = resp.status_code
    # db.session.add(new_result)
    db.session.commit()
    return


@app.route('/', methods=['GET', 'POST'])
def index():
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    form = SiteForm()
    if form.validate_on_submit():
        site_list = [x.strip() for x in form.sites.data.split(',')]
        for site in site_list:
            if not site.startswith('http'):
                site = f'http://{site}'
            new_task = Tasks(address=site, task_status=TaskStatus.NOT_STARTED)
            db.session.add(new_task)
            db.session.commit()
            py_counter.delay(new_task.id)
        return redirect(url_for('result'))
    return render_template('index.html', form=form)


@app.route('/result')
def result():
    results = Results.query.order_by(Results.id.desc()).limit(30).all()
    return render_template('result.html', results=results)


@app.route('/fresult')
def result_for_fetch():
    results = jsonify([x.serialize for x in Results.query.order_by(Results.id.desc()).limit(30).all()])
    return results


@app.route('/tasks')
def tasks():
    tasks = Tasks.query.order_by(Tasks.id.desc()).limit(40).all()
    return render_template('tasks.html', tasks=tasks)
