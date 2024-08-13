from .models import Profile,Ticket
def navbar_context(request):
    if request.user.is_authenticated:
        
        return {'Profile_menu': Profile.objects.filter(department=request.user.profile.department), 'Ticket_menu':Ticket.objects.filter(status__exact="INPROGRESS") }
    
    else:    
        return {}