import os
from app import app
from flask import Flask, render_template, redirect, flash, request, url_for, abort
from werkzeug.urls import url_encode
import requests
import json
import urllib
from app.models.forms import GetLead, DoLogin, InsertUser
from app.models.tables import User
from flask_login import login_user, LoginManager, current_user, login_required, logout_user
from is_safe_url import is_safe_url

from app import db



@app.route('/', defaults={'user': None})
@app.route('/index', defaults={'user': None})
@app.route('/index.html', defaults={'user': None})
def index(user):
    """Serve homepage template."""
    return render_template("pages/index.html", 
        user=user)


@app.route('/topic/<topic>', defaults={'user': None, 'topic': None})
def topic(user, topic):
    """Serve homepage template."""
    return render_template("pages/topic.html", 
        user=user, topic=topic)



@app.route('/content', defaults={'title': None})
@app.route('/content/<title>')
def _content(title):
    """Serve homepage template."""
    return render_template("pages/content.html", 
        title=title)


@app.route('/test', defaults={'name': None})
@app.route('/test/<name>')
def test(name):
    """Serve homepage template."""
    if name:
        return "Olá, %s!" % name
    else:
        return "Olá usuário"


'''def redirect_dest(fallback):
    dest = request.args.get('next')
    if not is_safe_url(dest):
        return abort(400)
    try:
        dest_url = url_for(dest)
    except:
        return redirect(fallback)
    return redirect(dest_url)'''


@app.route('/login', methods=['POST', 'GET'])
@app.route('/login.html', methods=['POST', 'GET'])
@app.route('/login.html?next=index', methods=['POST', 'GET'])

def login():
    """Serve homepage template."""
    form = DoLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            User.get_id(user)
            print(current_user)
            flash("Logged in!")
            #return redirect_dest(fallback=url_for('index', next=request.endpoint))
            next = request.args.get('next')
            #next = 'index'
            print(next)
            if not is_safe_url(next, {"127.0.0.1:5000"}):
                return abort(400)
            return redirect(next or url_for('index'))            
        else:
            flash("Invalid login.")
    else:
        print(form.errors)
    return render_template("forms/login.html", form=form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/register', methods=['POST', 'GET'])
def register():
    form = InsertUser()
    if form.validate_on_submit():
        i = User(form.data['name'], 
            form.data['username'],
            form.data['email'],
            form.data['password'],
            form.data['role'])
        db.session.add(i)
        db.session.commit()
        print('valido')
        return render_template('pages/index.html', form=form)
    else:
        print(form.errors)
    return render_template('forms/register.html', form=form)