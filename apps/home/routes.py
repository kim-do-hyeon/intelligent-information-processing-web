# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound


@blueprint.route('/index')
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/test')
def test():
    return render_template('home/about_professor_jo.html')

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