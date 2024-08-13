from django.urls import path
from . import views

from .views import create_customer,list_customer


urlpatterns = [

    path('',views.home,name='home'),
    path('my_queue/',views.my_queue,name='my_queue'),
    path('department_queue/',views.department_queue,name='department_queue'),
    path('all_queue/',views.all_queue,name='all_queue'),
    path('search_ticket/',views.search_ticket,name='search_ticket'),
    path('send_ticket/',views.send_ticket,name='send_ticket'),
    path('assign_to_person/<int:pk>/',views.assign_to_person,name='assign_to_person'),
    path('assign_to_department/<int:pk>/',views.assign_to_department,name='assign_to_department'),
    path('ticket_detail/<int:pk>/',views.ticket_detail,name='ticket_detail'),
    path('ticket_close/<int:pk>/',views.ticket_close,name='ticket_close'),
    path('update_ticket/<int:pk>/',views.update_ticket,name='update_ticket'),
    path('info_tables',views.info_tables,name="info_tables"),
    path('department_statistic',views.department_statistic,name='department_statistic'),
    path('create_department/',views.create_department,name='create_department'),
    path('update_department/<int:pk>/',views.update_department,name='update_department'),
    path('list_oncall_all',views.list_oncall_all,name="list_oncall_all"),
    path('list_oncall_dep',views.list_oncall_dep,name="list_oncall_dep"),
    path('create_user/',views.create_user,name='create_user'),
    path('list_users/',views.list_users,name='list_users'),
    path('list_dep_profiles/',views.list_dep_profiles,name='list_dep_profiles'),
    path('list_department/',views.list_department,name='list_department'),
    path('show_department/<int:pk>/',views.show_department,name='show_department'),
    path('list_workrole/',views.list_workrole,name='list_workrole'),
    path('create_workrole/',views.create_workrole,name='create_workrole'),
    path('create_customer/',views.create_customer,name='create_customer'),
    path('list_customer/',views.list_customer,name='list_customer'),
    path('show_account/<int:pk>/',views.show_account,name='show_account'),
    path('update_profile_admin/<int:pk>/',views.update_profile_admin,name='update_profile_admin'),
    path('update_profile/',views.update_profile,name='update_profile'),
    path('update_user/<int:pk>/',views.update_user,name='update_user'),
    path('update_workrole/<int:pk>/',views.update_workrole,name='update_workrole'),
    path('update_customer/<int:pk>',views.update_customer,name='update_customer'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('reset_password/<int:pk>/',views.reset_password,name='reset_password'),
    path('change_password/',views.change_password,name='change_password'),
    path('export',views.export_tickets_csv, name='export_tickets_csv'),
    path('ticket_chart/', views.ticket_chart, name='ticket_chart'),
    path('ticket_status_chart/', views.ticket_status_chart, name='ticket_status_chart'),
    path('ticket_status_chart_admin/', views.ticket_status_chart_admin, name='ticket_status_chart_admin'),
    path('ticket_chart_admin/', views.ticket_chart_admin, name='ticket_chart_admin'),

    path('queue_chart/',views.queue_chart,name='queue_chart'),
    path('inprog_chart/',views.inprog_chart,name='inprog_chart'),
    path('resolved_chart/',views.resolved_chart,name='resolved_chart'),
    path('closed_chart/',views.closed_chart,name='closed_chart'),

   
    
]

