import xml.etree.ElementTree as ET
import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import QRRegisterForm, LoginForm
from .models import Voter, Candidate

def index(request):
    return render(request, "index.html")

def results(request):
    winner = sorted(Candidate.objects.all(), key=lambda x: x.votes)[-1]
    if not request.user.is_authenticated:
        return redirect('login')
    elif request.user.voter.casted_vote:
        return render(request, "results.html", {'winner': winner, 'candidates': [(i.id, i) for i in Candidate.objects.all()]})
    else:
        return redirect('vote')

def vote(request):
    user = request.user
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        print(body)
        print(body["Candidate"])
        candidate = Candidate.objects.get(id=body["Candidate"])
        print(Candidate)
        if user.is_authenticated:
            if not user.voter.casted_vote:
                user.voter.casted_vote = True
                user.voter.save()
                candidate.votes += 1
                candidate.save()
                return redirect("index")
            else:
                return redirect("results")
        else:
            return redirect("login")
    else:
        if not user.is_authenticated:
            return redirect("login")
        elif user.voter.casted_vote:
            return redirect("results")
        else:
            return render(request, "castvote.html", {'candidates': [(i.id, i) for i in Candidate.objects.all()]})

def register(request):
    if request.method == 'POST':
        form = QRRegisterForm(request.POST)

        if form.is_valid():
            qr_data = form.cleaned_data.get('qr_data')
            aadhaar = form.cleaned_data.get('aadhaar')
            name = form.cleaned_data.get('name')
            dob = form.cleaned_data.get('dob')
            house = form.cleaned_data.get('house')
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            if aadhaar:
                username = aadhaar

                if User.objects.filter(username=username).exists():
                    form.add_error(None, "User already exists")
                    return render(request, 'register.html', {'form': form})

                if Voter.objects.filter(aadhaar=aadhaar).exists():
                    form.add_error('aadhaar', "This Aadhaar number is already registered")
                    return render(request, 'register.html', {'form': form})

                user = User.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password),
                )

                Voter.objects.create(
                    user=user,
                    name=name,
                    house=house or '',
                    dob=dob or '',
                    aadhaar=aadhaar
                )

                return redirect('login')

            try:
                root = ET.fromstring(qr_data)
                data = root.attrib
                username = data["uid"]

                address = ' '.join([
                    data.get("house", ""),
                    data.get("street", ""),
                    data.get("vtc", ""),
                    data.get("dist", "")
                ]).strip()

            except Exception:
                form.add_error('qr_data', 'Invalid QR XML data')
                return render(request, 'register.html', {'form': form})

            if User.objects.filter(username=username).exists():
                form.add_error(None, "User already exists")
                return render(request, 'register.html', {'form': form})

            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
            )

            Voter.objects.create(
                user=user,
                name=data.get("name", ""),
                house=address,
                dob=data.get("dob", ""),
                aadhaar=None
            )

            return redirect('login')

    else:
        form = QRRegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')
