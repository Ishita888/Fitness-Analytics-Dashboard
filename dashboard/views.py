from datetime import date, timedelta
from collections import defaultdict

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .forms import SignUpForm, DailyFitnessForm, ProfileForm
from .models import DailyFitnessEntry


def home(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(
        request,
        "dashboard/home.html"
    )


def signup(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = SignUpForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Account created successfully!"
            )

            return redirect("dashboard")

    else:

        form = SignUpForm()

    return render(
        request,
        "registration/signup.html",
        {"form": form}
    )


@login_required
def dashboard(request):

    entries = DailyFitnessEntry.objects.filter(
        user=request.user
    )

    today = date.today()

    today_entry = entries.filter(
        date=today
    ).first()

    last_7_days = today - timedelta(days=6)

    week_entries = entries.filter(
        date__range=[last_7_days, today]
    )

    last_30_days = today - timedelta(days=29)

    month_entries = entries.filter(
        date__range=[last_30_days, today]
    )

    # Basic statistics

    total_calories_burned = sum(
        e.calories_burned or 0
        for e in month_entries
    )

    total_food_intake = sum(
        e.food_intake or 0
        for e in month_entries
    )

    total_steps = sum(
        e.steps or 0
        for e in month_entries
    )

    avg_water = 0

    water_values = [
        e.water_intake
        for e in month_entries
        if e.water_intake is not None
    ]

    if water_values:
        avg_water = round(
            sum(water_values) / len(water_values),
            2
        )

    avg_sleep = 0

    sleep_values = [
        e.sleep_hours
        for e in month_entries
        if e.sleep_hours is not None
    ]

    if sleep_values:
        avg_sleep = round(
            sum(sleep_values) / len(sleep_values),
            2
        )

    # Chart data

    chart_entries = list(
        month_entries.order_by("date")
    )

    chart_dates = [
        e.date.strftime("%d %b")
        for e in chart_entries
    ]

    weight_data = [
        e.weight if e.weight is not None else None
        for e in chart_entries
    ]

    calories_data = [
        e.calories_burned or 0
        for e in chart_entries
    ]

    food_data = [
        e.food_intake or 0
        for e in chart_entries
    ]

    steps_data = [
        e.steps or 0
        for e in chart_entries
    ]

    water_data = [
        e.water_intake or 0
        for e in chart_entries
    ]

    sleep_data = [
        e.sleep_hours or 0
        for e in chart_entries
    ]

    context = {

        "today_entry": today_entry,

        "week_entries": week_entries,

        "month_entries": month_entries,

        "total_entries": entries.count(),

        "total_calories_burned":
            total_calories_burned,

        "total_food_intake":
            total_food_intake,

        "total_steps":
            total_steps,

        "avg_water":
            avg_water,

        "avg_sleep":
            avg_sleep,

        "chart_dates":
            chart_dates,

        "weight_data":
            weight_data,

        "calories_data":
            calories_data,

        "food_data":
            food_data,

        "steps_data":
            steps_data,

        "water_data":
            water_data,

        "sleep_data":
            sleep_data,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


@login_required
def add_entry(request):

    if request.method == "POST":

        form = DailyFitnessForm(request.POST)

        if form.is_valid():

            entry = form.save(commit=False)

            entry.user = request.user

            entry.exercises = form.cleaned_data["exercises"]

            entry.save()

            messages.success(
                request,
                "Fitness data saved successfully!"
            )

            return redirect("dashboard")

    else:

        form = DailyFitnessForm(
            initial={
                "date": date.today()
            }
        )

    return render(
        request,
        "dashboard/add_entry.html",
        {
            "form": form
        }
    )


@login_required
def history(request):

    entries = DailyFitnessEntry.objects.filter(
        user=request.user
    )

    return render(
        request,
        "dashboard/history.html",
        {
            "entries": entries
        }
    )


@login_required
def edit_entry(request, entry_id):

    entry = get_object_or_404(
        DailyFitnessEntry,
        id=entry_id,
        user=request.user
    )

    if request.method == "POST":

        form = DailyFitnessForm(
            request.POST,
            instance=entry
        )

        if form.is_valid():

            updated_entry = form.save(
                commit=False
            )

            updated_entry.user = request.user

            updated_entry.exercises = form.cleaned_data[
                "exercises"
            ]

            updated_entry.save()

            messages.success(
                request,
                "Fitness data updated!"
            )

            return redirect("history")

    else:

        form = DailyFitnessForm(
            instance=entry,
            initial={
                "exercises": entry.exercises
            }
        )

    return render(
        request,
        "dashboard/edit_entry.html",
        {
            "form": form,
            "entry": entry
        }
    )

@login_required
def delete_entry(
    request,
    entry_id
):

    entry = get_object_or_404(
        DailyFitnessEntry,
        id=entry_id,
        user=request.user
    )

    if request.method == "POST":

        entry.delete()

        messages.success(
            request,
            "Fitness entry deleted!"
        )

    return redirect("history")


@login_required
def profile(request):

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated!"
            )

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=request.user
        )

    return render(
        request,
        "dashboard/profile.html",
        {
            "form": form
        }
    )


@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Password changed successfully!"
            )

            return redirect("profile")

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        "dashboard/change_password.html",
        {
            "form": form
        }
    )