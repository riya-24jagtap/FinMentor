from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('input/', views.input_page, name='input'),
    path('compute/', views.compute_health, name='compute_health'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),

    # Dashboard routes
    path('spending/', views.spending_insights, name='spending'),
    path('loans-emi/', views.loans_emi, name='loans_emi'),
    path('action-plan/', views.action_plan, name='action_plan'),
    path('action-plan/predict/', views.action_plan_predict, name='action_plan_predict'),

    path('expenses/edit/', views.edit_expenses, name='edit_expenses'),
    path('savings/', views.savings_goals, name='savings'),
    path('savings/goals/add/', views.add_goal, name='add_goal'),
    path('savings/goals/<int:goal_id>/edit/', views.edit_goal, name='edit_goal'),
    path('savings/goals/<int:goal_id>/delete/', views.delete_goal, name='delete_goal'),

    # Auth
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/verify-otp/', views.verify_otp, name='verify_otp'),
    path(
        'accounts/password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'accounts/password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'accounts/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]