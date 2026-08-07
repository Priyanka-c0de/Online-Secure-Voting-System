import json
import xml.etree.ElementTree as ET

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import LoginForm, QRRegisterForm
from .models import Candidate, Voter


def index(request):
    return render(request, "index.html")


def results(request):
    if not request.user.is_authenticated:
        return redirect("login")

    candidates = Candidate.objects.all()

    if not candidates.exists():
        return render(
            request,
            "results.html",
            {"winner": None, "candidates": []},
        )

    winner = candidates.order_by("-votes").first()

    if request.user.voter.casted_vote:
        return render(
            request,
            "results.html",
            {
                "winner": winner,
                "candidates": [(i.id, i) for i in candidates],
            },
        )

    return redirect("vote")


def vote(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user

    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))

        candidate = Candidate.objects.get(id=body["Candidate"])

        if not user.voter.casted_vote:
            user.voter.casted_vote = True
            user.voter.save()

            candidate.votes += 1
            candidate.save()

            return redirect("index")

        return redirect("results")

    if user.voter.casted_vote:
        return redirect("results")

    return render(
        request,
        "castvote.html",
        {"candidates": [(i.id, i) for i in Candidate.objects.all()]},
    )


def register(request):
    if request.method == "POST":
        form = QRRegisterForm(request.POST)

        if form.is_valid():
            xml_data = form.cleaned_data["qr_data"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]

            try:
                root = ET.fromstring(xml_data)
                data = root.attrib

                username = data["uid"]

                address = " ".join(
                    [
                        data["house"],
                        data["street"],
                        data["vtc"],
                        data["dist"],
                    ]
                )

            except Exception:
                form.add_error("qr_data", "Invalid QR XML data")
                return render(request, "register.html", {"form": form})

            if User.objects.filter(username=username).exists():
                form.add_error(None, "User already exists")
                return render(request, "register.html", {"form": form})

            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
            )

            Voter.objects.create(
                user=user,
                name=data["name"],
                house=address,
                dob=data["dob"],
            )

            return redirect("register")

    else:
        form = QRRegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user is not None:
                login(request, user)
                return redirect("index")

            form.add_error(None, "Invalid username or password")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")


# ==========================================================
# Dashboard (Novelty Feature)
# ==========================================================


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    total_voters = Voter.objects.count()
    voted = Voter.objects.filter(casted_vote=True).count()
    pending = total_voters - voted

    turnout = 0
    if total_voters > 0:
        turnout = round((voted / total_voters) * 100, 2)

    candidates = Candidate.objects.all().order_by("-votes")

    winner = candidates.first() if candidates.exists() else None

    context = {
        "total_voters": total_voters,
        "voted": voted,
        "pending": pending,
        "turnout": turnout,
        "winner": winner,
        "candidates": candidates,
    }

    return render(request, "dashboard.html", context)
