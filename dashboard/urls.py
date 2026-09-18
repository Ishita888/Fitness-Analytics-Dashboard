from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "signup/",
        views.signup,
        name="signup"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "add-entry/",
        views.add_entry,
        name="add_entry"
    ),

    path(
        "history/",
        views.history,
        name="history"
    ),

    path(
        "edit/<int:entry_id>/",
        views.edit_entry,
        name="edit_entry"
    ),

    path(
        "delete/<int:entry_id>/",
        views.delete_entry,
        name="delete_entry"
    ),

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "change-password/",
        views.change_password,
        name="change_password"
    ),
]