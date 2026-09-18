from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm
)

from .models import DailyFitnessEntry


class SignUpForm(UserCreationForm):

    email = forms.EmailField(
        required=True
    )

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]


class DailyFitnessForm(forms.ModelForm):

    exercises = forms.MultipleChoiceField(
        choices=DailyFitnessEntry.EXERCISE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Exercises"
    )


    class Meta:

        model = DailyFitnessEntry

        fields = [
            "date",
            "weight",
            "height",
            "calories_burned",
            "food_intake",
            "steps",
            "water_intake",
            "sleep_hours",
            "exercises",
            "workout_duration",
            "fitness_goal",
        ]

        widgets = {

            "date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "weight": forms.NumberInput(
                attrs={
                    "placeholder": "Weight in kg",
                    "step": "0.1"
                }
            ),

            "height": forms.NumberInput(
                attrs={
                    "placeholder": "Height in cm",
                    "step": "0.1"
                }
            ),

            "calories_burned": forms.NumberInput(
                attrs={
                    "placeholder": "Calories burned"
                }
            ),

            "food_intake": forms.NumberInput(
                attrs={
                    "placeholder": "Calories consumed"
                }
            ),

            "steps": forms.NumberInput(
                attrs={
                    "placeholder": "Number of steps"
                }
            ),

            "water_intake": forms.NumberInput(
                attrs={
                    "placeholder": "Water in litres",
                    "step": "0.1"
                }
            ),

            "sleep_hours": forms.NumberInput(
                attrs={
                    "placeholder": "Sleep in hours",
                    "step": "0.1"
                }
            ),

            "workout_duration": forms.NumberInput(
                attrs={
                    "placeholder": "Duration in minutes"
                }
            ),
        }


class ProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "username",
            "email"
        ]