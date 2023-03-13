# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request, flash, redirect
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.models import students, Users
from werkzeug.utils import secure_filename
import os
from apps import db


@blueprint.route('/index')
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/about/<path:subpath>')
def about(subpath):
    parameter = subpath.split("/")
    print(parameter)
    if parameter[0] == 'professor' :
        if parameter[1] == 'jo-dong-young' :
            return render_template('home/about_professor_jo-dong-young.html')
        elif parameter[1] == 'jang-hong-jun' :
            return render_template('home/about_professor_jang-hong-jun.html')
    elif parameter[0] == 'lab' :
        if parameter[1] == 'intelligent' :
            return render_template('home/about-intelligent.html')
        elif parameter[1] == 'algorithm' :
            return render_template('home/about-algorithm.html')
        elif parameter[1] == 'intelligent-students' :
            return render_template('home/about-intelligent-students.html')
        elif parameter[1] == 'algorithm-students' :
            return render_template('home/about-algorithm-students.html')
    return str("Error" + parameter)

@blueprint.route('/project/<path:subpath>')
def project(subpath) :
    parameter=  subpath.split("/")
    print(parameter)
    if parameter[0] == "intelligent" :
        if parameter[1] == "intelligent-event-analysis" :
            return render_template('home/project/1-intelligent-event-analysis.html')
    return str(parameter)

@blueprint.route('/manage_users', methods = ['POST', 'GET'])
@login_required
def manage_users() :
    data = Users.query.filter_by().all()
    return render_template('home/user_lists.html', data = data)

@blueprint.route('/manage_students', methods = ['POST', 'GET'])
@login_required
def edit_students():
    if request.method == 'GET' :
        data = (students.query.filter_by().all())
        return render_template('home/add_students.html', data = data)
    elif request.method == 'POST' :
        form_username = (request.form['username'])
        form_position = (request.form['position'])
        form_lab = (request.form.get('lab'))
        form_description = (request.form['description'])
        form_image = request.files['image']
        if secure_filename(form_image.filename) == "" :
            file_path = None
        else :
            file_path = os.getcwd() + '/apps/students_image/' + secure_filename(form_image.filename)
            form_image.save(file_path)
        data = students(username = form_username, lab = form_lab,
                            position = form_position, description = form_description,
                            image = file_path)
        db.session.add(data)
        db.session.commit()
        flash("추가되었습니다.")
        return redirect('/manage_students')

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'
        segment = get_segment(request)
        return render_template("home/" + template, segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except:
        return render_template('home/page-500.html'), 500

def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None