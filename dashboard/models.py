from django.db import models
from django.contrib.auth.models import User


class DailyFitnessEntry(models.Model):

    GOAL_CHOICES = [
        ("Lose Weight", "Lose Weight"),
        ("Gain Weight", "Gain Weight"),
        ("Maintain Weight", "Maintain Weight"),
        ("Build Muscle", "Build Muscle"),
        ("Improve Fitness", "Improve Fitness"),
        ("Increase Strength", "Increase Strength"),
        ("Improve Endurance", "Improve Endurance"),
        ("General Health", "General Health"),
    ]

    EXERCISE_CHOICES = [
        ("Running", "Running"),
        ("Walking", "Walking"),
        ("Cycling", "Cycling"),
        ("Squats", "Squats"),
        ("Lunges", "Lunges"),
        ("Push-ups", "Push-ups"),
        ("Pull-ups", "Pull-ups"),
        ("Bench Press", "Bench Press"),
        ("Lat Pulldown", "Lat Pulldown"),
        ("Plank", "Plank"),
        ("Yoga", "Yoga"),
        ("Swimming", "Swimming"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    weight = models.FloatField(
        null=True,
        blank=True
    )

    height = models.FloatField(
        null=True,
        blank=True
    )

    calories_burned = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    food_intake = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    steps = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    water_intake = models.FloatField(
        null=True,
        blank=True
    )

    sleep_hours = models.FloatField(
        null=True,
        blank=True
    )

    # Multiple exercises can be selected
    exercises = models.JSONField(
        default=list,
        blank=True
    )

    workout_duration = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    fitness_goal = models.CharField(
        max_length=50,
        choices=GOAL_CHOICES,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_user_daily_entry"
            )
        ]

        ordering = ["-date"]


    def __str__(self):
        return f"{self.user.username} - {self.date}"


    @property
    def bmi(self):

        if self.weight and self.height and self.height > 0:

            height_m = self.height / 100

            return round(
                self.weight / (height_m ** 2),
                2
            )

        return None