import base64,io
from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """

""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image


# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("account"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, username=form.username.data, password=hashed_pwd)
        user.save()
        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)


# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("account"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is None:
            flash("No Username found!")
        elif not bcrypt.check_password_hash(user.password, form.password.data):
            flash("Incorrect Username/Password!")
        else:
            login_user(user)
            return redirect(url_for("movies.index"))

    return render_template("login.html", form=form)


# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            # TODO: handle update username form submit
            newUser = User.objects(username=update_username_form.username.data).first()

            if newUser is None:
                current_user.username = update_username_form.username.data
                current_user.save()
                return redirect("account")

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            # TODO: handle update profile pic form submit
            img = update_profile_pic_form.picture.data
            filename = secure_filename(img.filename)
            content_type = f'images/{filename[-3:]}'

            if current_user.profile_pic.get() is None:
                current_user.profile_pic.put(img.stream, content_type=content_type)
            else:
                current_user.profile_pic.replace(img.stream, content_type=content_type)
            current_user.save()
            return redirect("account")

    # TODO: handle get requests
    return render_template("account.html", update_username_form=update_username_form, update_profile_pic_form=update_profile_pic_form, image=get_b64_img(current_user.username))