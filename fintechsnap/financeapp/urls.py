from django.urls import path
from django.contrib.auth import views as auth_views
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

    # 🔥 THIS WAS MISSING
    path(
        'action-plan/predict/',
        views.action_plan_predict,
        name='action_plan_predict'
    ),

    path('expenses/edit/', views.edit_expenses, name='edit_expenses'),
    path('savings/', views.savings_goals, name='savings'),
    path('savings/goals/add/', views.add_goal, name='add_goal'),
    path('savings/goals/<int:goal_id>/edit/', views.edit_goal, name='edit_goal'),
    path('savings/goals/<int:goal_id>/delete/', views.delete_goal, name='delete_goal'),

    # Auth
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('create-user/', views.force_create_user),
    
    
]
