from flask import Blueprint
from flask import render_template, request
from flask_login import login_user, logout_user, current_user, login_required


auth = Blueprint("auth", __name__)


@auth.route("/login/<uid>")
def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("base"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")



@auth.route("/logout")
def logout():
    return "<h1>Logout</h1>"


@auth.route("/register")
def signup():
    return "<h1>Sign up</h1>"
