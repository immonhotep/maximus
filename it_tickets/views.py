from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from  django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .decorators import user_is_superuser, user_not_authenticated,user_is_siteadmin
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
import csv
import datetime
from django.views import View



@login_required(login_url='user_login')
def home(request):

    if  request.user.is_superuser  or  request.user.profile.department_manager : 

        departments =  Department.objects.all() 

        if request.method == "POST":

            select_chart = request.POST.get('select_chart')
            request.session['select_chart'] = select_chart
            

        context={'departments':departments}
        return render(request,'tickets/admin_dashboard.html',context)          

    else:

        return render(request,'tickets/dashboard.html')

       
    



@login_required(login_url='user_login')
def department_queue(request):

    profiles = Profile.objects.filter(department=request.user.profile.department)
    tickets = Ticket.objects.filter(resolver_department=request.user.profile.department).order_by('opened').exclude(status__exact="CLOSED")

    p = Paginator(tickets,10)
    page = request.GET.get('page')
    tickets = p.get_page(page)

    
    context={'tickets':tickets,'group':'group','profiles':profiles}
    return render(request,'tickets/tickets.html',context)


@login_required(login_url='user_login')
def my_queue(request):

    tickets = Ticket.objects.filter(resolver_profile=request.user.profile).order_by('opened').exclude(status__exact="CLOSED")
    p = Paginator(tickets,10)
    page = request.GET.get('page')
    tickets = p.get_page(page)

    context={'tickets':tickets,'own':'own'}
    return render(request,'tickets/tickets.html',context)



@user_is_superuser
@login_required(login_url='user_login')
def all_queue(request):

    profiles = Profile.objects.filter(department=request.user.profile.department)


    selection = request.GET.get('list_radio')

    if selection == "INFO":
        request.session['selection'] = "INFO"
        tickets = Ticket.objects.filter(priority__exact="INFO").order_by('opened')
    elif selection == "WARNING":
        request.session['selection'] = "WARNING"
        tickets = Ticket.objects.filter(priority__exact="WARNING").order_by('opened')
    elif selection == "CRITICAL":
        request.session['selection'] = "CRITICAL"
        tickets = Ticket.objects.filter(priority__exact="CRITICAL").order_by('opened')
    elif selection == "FATAL":
        request.session['selection'] = "FATAL"
        tickets = Ticket.objects.filter(priority__exact="FATAL").order_by('opened')
    else:
        request.session['selection'] = "ALL"
        tickets = Ticket.objects.all().order_by('opened')
        



    p = Paginator(tickets,8)
    page = request.GET.get('page')
   
    try:
        tickets = p.page(page)
    except PageNotAnInteger:
        tickets = p.page(1)
    except EmptyPage:
        tickets = p.page(p.num_pages)


    context={'tickets':tickets,'all':'All','profiles':profiles,'selection':selection}
    return render(request,'tickets/tickets.html',context)



@login_required(login_url='user_login')
@user_is_superuser
def export_tickets_csv(request):

    selection = request.session.get('selection')

    if selection == "INFO":
        tickets = Ticket.objects.filter(priority__exact="INFO").order_by('opened')
    elif selection == "WARNING":
        tickets = Ticket.objects.filter(priority__exact="WARNING").order_by('opened')
    elif selection == "CRITICAL":
        tickets = Ticket.objects.filter(priority__exact="CRITICAL").order_by('opened')
    elif selection == "FATAL":
        tickets = Ticket.objects.filter(priority__exact="FATAL").order_by('opened')
    else:
        tickets = Ticket.objects.all().order_by('opened')

    if not tickets.exists():
        messages.error(request,'No item to export')
        return redirect('all_queue')
    
    time = str(datetime.datetime.now()).replace(' ','--')

    response = HttpResponse(content_type='text/csv')
     
    response['Content-Disposition'] = f"attachment; filename='{time}-tickets.csv'"
    
    writer = csv.writer(response,delimiter =";",quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Ticket ID','Title', 'Dispacher department', 'Dispacher profile', 'Resolver department', 'Resolver profile', 'Priority', 'Status','Opened'])

   
    for ticket in tickets:
                       
         ticketlist = [ticket.ticket_id,ticket.title,ticket.dispacher_department,ticket.dispacher_profile,ticket.resolver_department,ticket.resolver_profile,ticket.priority,ticket.status,ticket.opened]
              
         writer.writerow(ticketlist)

    return response






@login_required(login_url='user_login')
def search_ticket(request):

    
    if request.method == "GET":

        searching = request.GET.get('search')
        

        tickets = Ticket.objects.filter(Q(ticket_id__icontains=searching) | Q(title__icontains=searching) | Q(ticket_description__icontains=searching)
             |   Q(priority__icontains=searching) | Q(status__icontains=searching)  ).order_by('opened')
        

        if not tickets:
            messages.error(request,f'Not found any ticket with {searching}')
            return redirect('home')
        

        p = Paginator(tickets,8)
        page = request.GET.get('page')
        
        try:
            tickets = p.page(page)
        except PageNotAnInteger:
            tickets = p.page(1)
        except EmptyPage:
            tickets = p.page(p.num_pages)

        

        context={'tickets':tickets,'search':'search'}
        return render(request,'tickets/tickets.html',context)
    
    return redirect('home')





@login_required(login_url='user_login')
def ticket_detail(request,pk):

    ticket = get_object_or_404(Ticket,pk=pk)



    profiles = Profile.objects.filter(department=request.user.profile.department)
    departments = Department.objects.all()

    if request.user.profile.department != ticket.resolver_department:
        messages.info(request,'Ticket read only not in your department queue')

        
    if request.user.profile == ticket.resolver_profile:

            if request.method == "POST":

                select = request.POST.get('inlineRadioOptions')
                

                form = SetResolutionForm(request.POST,instance=ticket)
            

                if  form.is_valid():
                    data = form.save(commit=False)
                    
                    time = str(datetime.datetime.now()).replace(' ','--')
                    format ="  \r---Updated -"+time+"-(by:"+request.user.first_name+"-"+request.user.last_name+")"
                    data.resolution_status+=format


                    if select == "Resolve":
                        data.status =  "RESOLVED"
                        messages.success(request,f'You resolved the ticket: {ticket.ticket_id}')

                    else:
                        messages.success(request,f'You updated the ticket: {ticket.ticket_id}')

                
                    data.save()

                    
                    return redirect('my_queue')
                
                else:
                    for error in list(form.errors.values()):
                        messages.error(request,error)
                        return redirect(ticket_detail,pk)
            
            else:
                form = SetResolutionForm(instance=ticket)
                context = {'ticket':ticket,'form':form,'profiles':profiles,'departments':departments}
                return render(request,'tickets/ticket_detail.html',context)
            



    context = {'ticket':ticket,'profiles':profiles,'departments':departments}
    return render(request,'tickets/ticket_detail.html',context)
    




@login_required(login_url='user_login')
def ticket_close(request,pk):

      
 
    ticket = get_object_or_404(Ticket,pk=pk)

   
    if request.user.profile.department_manager:

        if  request.method == "POST":

            closed = request.POST.get('close_ticket')
            

            if closed == "Close":
                    ticket.status = "CLOSED"
                    ticket.save()
                    messages.success(request,f'You closed the ticket {ticket.ticket_id}')
                    return redirect(request.META.get('HTTP_REFERER'))
            
    return redirect('home')


@login_required(login_url='user_login')
@user_is_superuser
def update_ticket(request,pk):

    ticket = get_object_or_404(Ticket,pk=pk)


    if request.method == "POST":

        form = AdminUpdateTicketform(request.POST,instance=ticket)
        if form.is_valid():
                form.save()
                messages.success(request,f'Ticket {ticket.ticket_id} updated')
                return redirect('update_ticket',pk)

        else:
            for error in  list(form.errors.values()):
                messages.error(request,error)
    else:

        form = AdminUpdateTicketform(instance=ticket)

    context={'form':form}
    return render(request,'tickets/update_ticket.html',context)




@login_required(login_url='user_login')
def send_ticket(request):

    if request.method == "POST":

        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.dispacher_department = request.user.profile.department
            data.dispacher_profile = request.user.profile
            data.save()
            messages.success(request,f'{data.ticket_id}  has been sent to {data.resolver_department}')
            return redirect('home')
            

        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    else:
        form = TicketForm()
    context={'form':form}
    return render(request,'tickets/send_ticket.html',context)



@login_required(login_url='user_login')
def assign_to_person(request,pk):

    ticket = get_object_or_404(Ticket,pk=pk)

    if request.method == "POST":

        if request.user.profile.department != ticket.resolver_department:
            messages.error(request,'You have not permission to do that')
            return redirect('home')

        to_person = request.POST.get('profiles')
        

        profile = Profile.objects.get(pk=to_person)

        ticket.resolver_profile = profile
        ticket.status = "INPROGRESS"
        ticket.save()
        messages.success(request,f'{ticket.ticket_id} successfully assigned to user: {profile.user.username}' )
        return redirect('department_queue')


@login_required(login_url='user_login')
def assign_to_department(request,pk):

    ticket = get_object_or_404(Ticket,pk=pk)

    if request.method == "POST":

        if request.user.profile.department != ticket.resolver_department:
            messages.error(request,'You have not permission to do that')
            return redirect('home')

        to_department = request.POST.get('departments')
        

        department = Department.objects.get(pk=to_department)

        ticket.resolver_department = department
        ticket.status = "QUEUED"
        ticket.resolver_profile = None
        ticket.save()
        messages.success(request,f'{ticket.ticket_id} successfully assigned to department: {department.name}' )
        return redirect('department_queue')




@user_not_authenticated
def user_login(request):

        if request.method == "POST":

            username = request.POST['username']
            password = request.POST['password']


            user = authenticate(username=username,password=password)
       

            if user is not None:

                

                login(request,user)
                user.profile.log_count+=1
                user.profile.save()
                messages.success(request,f'welcome {username} this is your {user.profile.log_count} visit on the site')
                if user.profile.log_count == 1:
                    messages.info(request,'After first login please check your profile and change your password')
                    return redirect('update_profile')


                if request.user.is_superuser:
                    if user.profile.log_count == 1:
                        messages.info(request,'After first login Admin user need add at least one customer,workrole, and department')
                        return redirect('create_customer')

                return redirect('home')
            
            else:
                
                messages.error(request,'Invalid username or password')
                return redirect('user_login')

        return render(request,'tickets/user_login.html')


@login_required(login_url='user_login')
def user_logout(request):
    
    logout(request)
    messages.success(request,'You logged out')
    return redirect('home')


@login_required(login_url='user_login')
def update_profile(request):

    profile = request.user.profile

    if request.method == "POST":

        form = ProfileUserForm(request.POST,request.FILES,instance=profile)

        if form.is_valid():
                form.save()
                messages.success(request,'Profile has been updated')
                return redirect('home')

        else:
            for error in  list(form.errors.values()):
                messages.error(request,error)
    else:

        form = ProfileUserForm(instance=profile)

    context={'form':form}
    return render(request,'tickets/update_profile.html',context)





        
@login_required(login_url='user_login')
@user_is_siteadmin
def update_profile_admin(request,pk):

    profile = get_object_or_404(Profile,pk=pk)

    if request.method == "POST":
            form = ProfileAdminForm(request.POST,request.FILES,instance=profile)   
            if form.is_valid():
                form.save()
                messages.success(request,f'Profile {profile.user.username} has been updated')
                return redirect('list_users')

            else:

                for error in  list(form.errors.values()):
                    messages.error(request,error)
    else:
        form = ProfileAdminForm(instance=profile)
            

    context={'form':form}
    return render(request,'tickets/update_profile_admin.html',context)







@login_required(login_url='user_login')
@user_is_siteadmin
def create_user(request):

    if request.method == "POST":

        form = AdminUserCreationForm(request.POST)

        

        if form.is_valid():

            data=form.save()
        
            messages.success(request,'User has been created')
            return redirect('update_profile_admin',data.profile.pk)


        else:
            
            for error in list(form.errors.values()):
                messages.error(request,error)         

            
    else:
        form = AdminUserCreationForm()
        


    context={'form':form,'create':'Create new'}
    return render(request,'tickets/create_user.html',context)


@login_required(login_url='user_login')
@user_is_siteadmin
def update_user(request,pk):
   
   user = get_object_or_404(User,pk=pk)

   if request.method == "POST":
        
        form = AdminUserupdateForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,f'You updated the profile:{user.username}')
            return redirect('list_users')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    
                return redirect('list_users')
   else:
       
       form = AdminUserupdateForm(instance=user)

   context={'form':form,'modify':'Modify'}
   return render(request,'tickets/create_user.html',context)


@login_required(login_url='user_login')
def show_account(request,pk):

    account_profile = get_object_or_404(Profile,pk=pk)
    account_user = get_object_or_404(User,pk=account_profile.user.pk)


    if request.method == "POST":
            if request.user.profile.department_manager and account_profile.department == request.user.profile.department:
                form = ManagerupdateoncallForm(request.POST,instance=account_profile)
                if form.is_valid():
                    form.save()
                    messages.success(request,'Oncall status changed')
                else:
                    messages.error(request,'an error occurred')
            else:
                form = ManagerupdateoncallForm(instance=account_profile)
                messages.error(request,'Permission denied')

    else:
        form = ManagerupdateoncallForm(instance=account_profile)
       


    context={'account_profile':account_profile,'account_user':account_user,'form':form}
    return render(request,'tickets/show_account.html',context)


       
@login_required(login_url='user_login')
@user_is_siteadmin     
def reset_password(request,pk):

    user = get_object_or_404(User,pk=pk)

    if request.method == "POST":

        form = ResetUserPasswordForm(user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,f'{form.user} password reseted')
            return redirect('update_profile_admin',user.profile.pk)

        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('reset_password',pk)
    else:

        form = ResetUserPasswordForm(user)

    context={'form':form,'user':user}
    return render(request,'tickets/reset_password.html',context)


@login_required(login_url='user_login')          
def change_password(request):

    user = request.user

    if request.method == "POST":

        form = ChangeUserPasswordForm(user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,f'{form.user} password changed')
            return redirect('update_profile')

        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('change_password')

    else:

        form = ChangeUserPasswordForm(user)

    context={'form':form,'user':user}
    return render(request,'tickets/reset_password.html',context)

        
    


@login_required(login_url='user_login')
@user_is_superuser
def list_users(request):

    all_users  = User.objects.all().order_by('username')

    p = Paginator(all_users,10)
    page = request.GET.get('page')
    all_users = p.get_page(page)

    context = {'all_users':all_users}
    return render(request,'tickets/list_users.html',context)



@login_required(login_url='user_login')
def list_dep_profiles(request):

    department = request.user.profile.department
    dep_profiles  = Profile.objects.filter(department=department).order_by('user')

    p = Paginator(dep_profiles,10)
    page = request.GET.get('page')
    dep_profiles = p.get_page(page)

    context = {'dep_profiles':dep_profiles}
    return render(request,'tickets/list_profiles_dep.html',context)



@login_required(login_url='user_login')
@user_is_siteadmin
def create_department(request):

    if request.method == "POST":

        form = AdminDepartmentCreateForm(request.POST)
        if form.is_valid():

            data=form.save()
            messages.success(request,f'Department created: {data.name}')
            return redirect('home')
        
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    else:

        form = AdminDepartmentCreateForm()


    context={'form':form,'create':'Create'}
    return render(request,'tickets/create_department.html',context)


@login_required(login_url='user_login')
@user_is_siteadmin
def update_department(request,pk):

    department = get_object_or_404(Department,pk=pk)

    if request.method == "POST":

        form = AdminDepartmentCreateForm(request.POST,instance=department)
        if form.is_valid():
            form.save()
            messages.success(request,f'{department.name} has been updated')
            return redirect('list_department')
        else:

            for error in list(form.errors.values()):
                messages.error(request,error)
    else:

        form = AdminDepartmentCreateForm(instance=department)

    context={'form':form,'update':'Update'}
    return render(request,'tickets/create_department.html',context)


@login_required(login_url='user_login')
@user_is_superuser
def list_department(request):

    departments = Department.objects.all().order_by('name')

    p = Paginator(departments,10)
    page = request.GET.get('page')
    departments = p.get_page(page)

    
    context={'departments':departments}
    return render(request,'tickets/list_department.html',context)



@login_required(login_url='user_login')
@user_is_superuser
def show_department(request,pk):

    department = get_object_or_404(Department,pk=pk)
    dep_profiles = Profile.objects.filter(department=department)

   

    context={'department':department,'dep_profiles':dep_profiles}
    return render(request,'tickets/show_department.html',context)


def list_oncall_all(request):

    profiles = Profile.objects.filter(on_call_person=True)

    context={'dep_profiles':profiles,'oncall_all':'oncall_all'}
    return render(request,'tickets/list_profiles_dep.html',context)


def list_oncall_dep(request):

    department = request.user.profile.department
    
    profiles = Profile.objects.filter(on_call_person=True,department=department)

    context={'dep_profiles':profiles,'oncall_dep':'oncall_dep'}
    return render(request,'tickets/list_profiles_dep.html',context)






@login_required(login_url='user_login')
@user_is_siteadmin
def create_workrole(request):

    if request.method == "POST":

        form = WorkroleForm(request.POST)
        if form.is_valid():
            data=form.save()
            messages.success(request,f'{data.name} has been created')
            if request.user.is_superuser:
                if request.user.profile.log_count == 1:
                    return redirect('create_department')
                else:
                    return redirect('home')
            else:
                return redirect('home')

        else:
            for error in list(form.errors.values()):

                messages.error(request,error)
            

    else:

        form = WorkroleForm()



    context={'form':form}
    return render(request,'tickets/create_workrole.html',context)



@login_required(login_url='user_login')
@user_is_superuser
def list_workrole(request):

    workroles = Workrole.objects.all().order_by('name')

    context = {'workroles':workroles}
    return render(request,'tickets/list_workrole.html',context)



@login_required(login_url='user_login')
@user_is_siteadmin
def update_workrole(request,pk):

    workrole = get_object_or_404(Workrole,pk=pk)

    if request.method == "POST":

        form = WorkroleForm(request.POST,instance=workrole)
        if form.is_valid():
            data=form.save()
            messages.success(request,f'The workrole {data.name} updated')
            return redirect('list_workrole')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect(update_workrole,pk)
    else:

        form = WorkroleForm(instance=workrole)




    context={'form':form}
    return render(request,'tickets/update_workrole.html',context)



@login_required(login_url='user_login')
@user_is_siteadmin
def create_customer(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)
        if form.is_valid():
            data=form.save()
            messages.success(request,f'{data.name} customer created')
            if request.user.is_superuser:
                if request.user.profile.log_count == 1:
                    return redirect('create_workrole')


            return redirect('home')
        
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('home')
            
    else:

        form = CustomerForm()


    context={'form':form}
    return  render(request,'tickets/create_customer.html',context)


@login_required(login_url='user_login')
@user_is_superuser
def list_customer(request):

    customers = Customer.objects.all()

    context={'customers':customers}
    return  render(request,'tickets/list_customer.html',context)




@login_required(login_url='user_login')
@user_is_siteadmin
def update_customer(request,pk):

    customer = get_object_or_404(Customer,pk=pk)

    if request.method == "POST":

        form = CustomerForm(request.POST,instance=customer)

        if form.is_valid():
            data=form.save()
            messages.success(request,f'{data.name} customer has been modified')
            return redirect('list_customer')

        else:

            for error in list(form.errors.values()):

                messages.error(request,error)

    else:
        form = CustomerForm(instance=customer)


    context={'form':form}
    return render(request,'tickets/update_customer.html',context)





@login_required(login_url='user_login')
@user_is_superuser
def info_tables(request):


    departments = Department.objects.all()
    tickets = Ticket.objects.all()
    

   
    department_select = request.GET.get('select_department')
    

    if department_select != "all" and department_select != None:
        tickets = Ticket.objects.filter(resolver_department__id=department_select)


    opened_tickets = tickets.exclude(status__exact="CLOSED").order_by('-priority')
    closed_tickest = tickets.filter(status__exact="CLOSED").order_by('-priority')


    p = Paginator(opened_tickets,8)
    page = request.GET.get('page1')

    try:
        opened_tickets = p.page(page)
    except PageNotAnInteger:
        opened_tickets = p.page(1)
    except EmptyPage:
        opened_tickets = p.page(p.num_pages)



    l = Paginator(closed_tickest,8)
    page = request.GET.get('page2')
    
    try:
        closed_tickest = l.page(page)
    except PageNotAnInteger:
        closed_tickest = l.page(1)
    except EmptyPage:
        closed_tickest = l.page(l.num_pages)



    context={'opened_tickets':opened_tickets,'closed_tickest':closed_tickest,'departments':departments}
    return render(request,'tickets/info_tables.html',context)


@login_required(login_url='user_login')
def department_statistic(request):

    tickets = Ticket.objects.filter(resolver_department=request.user.profile.department)

    queued = tickets.filter(status__exact="QUEUED")
    inprog = tickets.filter(status__exact="INPROGRESS")
    resolved = tickets.filter(status__exact="RESOLVED")
    closed = tickets.filter(status__exact="CLOSED")


    priority_list=['INFO','WARNING','CRITICAL','FATAL']
    
    

    queue_list = [queued.count(),]
    inprog_list = [inprog.count(),]
    resolved_list = [resolved.count(),]
    closed_list = [closed.count(),]


   
    for item in priority_list:

        value = queued.filter(priority__exact=item).count()
        queue_list.append(value)


    for item in priority_list:

        value = inprog.filter(priority__exact=item).count()
        inprog_list.append(value)

    for item in priority_list:

        value = resolved.filter(priority__exact=item).count()
        resolved_list.append(value)

    for item in priority_list:

        value = closed.filter(priority__exact=item).count()
        closed_list.append(value)

    request.session['labels'] = priority_list
    request.session['queued_data'] = queue_list[1:5]
    request.session['inprog_data'] = inprog_list[1:5]
    request.session['resolved_data'] = resolved_list[1:5]
    request.session['closed_data'] = closed_list[1:5]

   
    
    context={'tickets':tickets,'queue_list':queue_list,'inprog_list':inprog_list,'resolved_list':resolved_list,'closed_list':closed_list}
    return render(request,'tickets/statistic.html',context)    
    

@login_required(login_url='user_login')
def queue_chart(request):

    labels = request.session.get('labels')
    data = request.session.get('queued_data')

    return JsonResponse(data={
        'labels': labels,
        'data': data,})


@login_required(login_url='user_login')
def inprog_chart(request):

    labels = request.session.get('labels')
    data = request.session.get('inprog_data')

    return JsonResponse(data={
        'labels': labels,
        'data': data,})


@login_required(login_url='user_login')
def resolved_chart(request):

    labels = request.session.get('labels')
    data = request.session.get('resolved_data')

    return JsonResponse(data={
        'labels': labels,
        'data': data,})

@login_required(login_url='user_login')
def closed_chart(request):

    labels = request.session.get('labels')
    data = request.session.get('closed_data')

    return JsonResponse(data={
        'labels': labels,
        'data': data,})









    

@login_required(login_url='user_login')
def ticket_chart(request):

    ticket = Ticket.objects.all()

    tickets_info = ticket.filter(resolver_department=request.user.profile.department,priority__exact="INFO").count()
    tickets_warning = ticket.filter(resolver_department=request.user.profile.department,priority__exact="WARNING").count()
    tickets_critical = ticket.filter(resolver_department=request.user.profile.department,priority__exact="CRITICAL").count()
    tickets_fatal = ticket.filter(resolver_department=request.user.profile.department,priority__exact="FATAL").count()

    labels = ['INFO','WARNING','CRITICAL','FATAL']
    data = [tickets_info,tickets_warning,tickets_critical,tickets_fatal]

    return JsonResponse(data={
        'labels': labels,
        'data': data,})


@user_is_superuser
@login_required(login_url='user_login')
def ticket_chart_admin(request):

    chart_select = request.session.get('select_chart')


    ticket = Ticket.objects.all()

    all_tickets = ticket.count()

    if chart_select != "all" and chart_select != None:

        ticket = Ticket.objects.filter(resolver_department__id=chart_select)


   

    
 


    tickets_info = ticket.filter(priority__exact="INFO").count() 
    tickets_warning = ticket.filter(priority__exact="WARNING").count() 
    tickets_critical = ticket.filter(priority__exact="CRITICAL").count() 
    tickets_fatal = ticket.filter(priority__exact="FATAL").count() 
    
   

    labels = ['INFO','WARNING','CRITICAL','FATAL']
    data = [tickets_info,tickets_warning,tickets_critical,tickets_fatal]
    

    return JsonResponse(data={
        'labels': labels,
        'data': data,
        })

@login_required(login_url='user_login')
def ticket_status_chart(request):

    ticket = Ticket.objects.all()

    tickets_queued = ticket.filter(resolver_department=request.user.profile.department,status__exact="QUEUED").count()
    tickets_inprog = ticket.filter(resolver_department=request.user.profile.department,status__exact="INPROGRESS").count()
    tickets_resolved = ticket.filter(resolver_department=request.user.profile.department,status__exact="RESOLVED").count()
    tickets_closed = ticket.filter(resolver_department=request.user.profile.department,status__exact="CLOSED").count()


    labels = ['QUEUED','INPROGRESS','RESOLVED','CLOSED']
    data = [tickets_queued,tickets_inprog,tickets_resolved,tickets_closed]

    return JsonResponse(data={
        'labels': labels,
        'data': data,})


@user_is_superuser
@login_required(login_url='user_login')
def ticket_status_chart_admin(request):

    chart_select = request.session.get('select_chart')

    ticket = Ticket.objects.all()

    if chart_select != "all" and chart_select != None:

        ticket = Ticket.objects.filter(resolver_department__id=chart_select)
        
        
  
    tickets_queued = ticket.filter(status__exact="QUEUED").count()
    tickets_inprog = ticket.filter(status__exact="INPROGRESS").count()
    tickets_resolved = ticket.filter(status__exact="RESOLVED").count()
    tickets_closed = ticket.filter(status__exact="CLOSED").count()

    labels = ['QUEUED','INPROGRESS','RESOLVED','CLOSED']
    data = [tickets_queued,tickets_inprog,tickets_resolved,tickets_closed]

    return JsonResponse(data={
        'labels': labels,
        'data': data,})

