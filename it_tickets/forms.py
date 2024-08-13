from django import forms
from .models import Ticket,Department,Profile,Workrole,User,Customer
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm,PasswordChangeForm

class TicketForm(forms.ModelForm):

    
    title = ticket_description = forms.CharField(widget=forms.TextInput(attrs={
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }))

    ticket_description = forms.CharField(widget=forms.Textarea(attrs={
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }))

    resolver_department = forms.ModelChoiceField(queryset=Department.objects.all(),widget=forms.Select(attrs={
          'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
     }),required=True)
      

    customer = forms.ModelChoiceField(queryset=Customer.objects.all(),widget=forms.Select(attrs={
          'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
     }),required=True)

    
    priority = forms.ChoiceField(choices=Ticket.TicketPriority.choices,widget=forms.Select(attrs={
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }) )


    
    class Meta:
        model = Ticket
        fields = ('title','ticket_description','resolver_department','customer','priority')


class TicketAssignForm(forms.ModelForm):

    resolver_profile = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(attrs={
          'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
     }),required=True)


    class Meta:
        model = Ticket
        fields = ('resolver_profile',)


class AdminUpdateTicketform(forms.ModelForm):

    dispacher_department  = forms.ModelChoiceField(queryset=Department.objects.all(),widget=forms.Select(attrs={
          'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
     }),required=True)
    

    dispacher_profile = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(attrs={
          'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
     }),required=True)


    title = ticket_description = forms.CharField(widget=forms.TextInput(attrs={
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }))

    ticket_description = forms.CharField(widget=forms.Textarea(attrs={
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }))


    customer = forms.ModelChoiceField(queryset=Customer.objects.all(),widget=forms.Select(attrs={
          'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
     }),required=True)

    resolver_department = forms.ModelChoiceField(queryset=Department.objects.all(),widget=forms.Select(attrs={
          'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
     }),required=True)
    
  

    resolver_profile = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(attrs={
          'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
     }),required=False)
    
    
    priority = forms.ChoiceField(choices=Ticket.TicketPriority.choices,widget=forms.Select(attrs={
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }) )


    status = forms.ChoiceField(choices=Ticket.Resolution_Status.choices,widget=forms.Select(attrs={
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }) )


    class Meta:
        model = Ticket
        fields = ('dispacher_department','dispacher_profile','title','ticket_description','customer','resolver_department','resolver_profile','priority','status')

   
    

class ProfileUserForm(forms.ModelForm):

    
    bio = forms.CharField(widget=forms.Textarea(attrs={
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }))


    class Meta:
        model = Profile
        fields = ('bio','avatar','on_call_person')



    
class ProfileAdminForm(forms.ModelForm):

    

    department = forms.ModelChoiceField(queryset=Department.objects.all(),widget=forms.Select(attrs={
          'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
          
     }),required=True)
    
    workrole = forms.ModelMultipleChoiceField(
        queryset=Workrole.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            
        })
    )
    
    bio = forms.CharField(widget=forms.Textarea(attrs={
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }))

    department_manager = forms.BooleanField(label='manager',required=False,widget=forms.CheckboxInput(attrs={
        
    }))

    on_call_person = forms.BooleanField(label='oncall',required=False,widget=forms.CheckboxInput(attrs={
        
    }))

    class Meta:
        model = Profile
        fields = ('department','workrole','bio','department_manager','on_call_person','avatar')


class AdminUserCreationForm(UserCreationForm) :


    username = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Username',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))


    first_name = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'First name ',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Last name ',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={

        'placeholder':'Email',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Phone Number ',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))

    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={

        'placeholder':' Password',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'  


    }))


    password2 = forms.CharField(label='Password confirm',widget=forms.PasswordInput(attrs={
    

        'placeholder':' Repeat Password',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'  


    }))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','phone')



class AdminUserupdateForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Username',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))


    first_name = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'First name ',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Last name ',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={

        'placeholder':'Email',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Phone Number ',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))

    is_active = forms.BooleanField

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','phone','is_active')



class ResetUserPasswordForm(SetPasswordForm):


    new_password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={

        'placeholder':' Password',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'  


    }))


    new_password2 = forms.CharField(label='Password confirm',widget=forms.PasswordInput(attrs={
    

        'placeholder':' Repeat Password',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'  

    }))


    class Meta:
        model = User

        fields=('new_password1','new_password2')


class ChangeUserPasswordForm(PasswordChangeForm):


    old_password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={

        'placeholder':'Old Password',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'  


    }))


    new_password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={

        'placeholder':' Password',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'  


    }))


    new_password2 = forms.CharField(label='Password confirm',widget=forms.PasswordInput(attrs={
    

        'placeholder':' Repeat Password',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'  

    }))


    class Meta:
        model = User

        fields=('old_password','new_password1','new_password2')



class SetResolutionForm(forms.ModelForm):


    resolution_status = forms.CharField(widget=forms.Textarea(attrs={
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }))

    class Meta:
        model = Ticket
        fields=('resolution_status',)


class AdminDepartmentCreateForm(forms.ModelForm):
        


    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Department name ',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))

    short_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Short name ',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))


        
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder':'Description',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }))

    class Meta:
        model = Department
        fields = ('name','short_name','description')
        
     
        
    
class WorkroleForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Workrole name ',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))
        
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder':'Description',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }))

    class Meta:
        model = Workrole
        fields = ('name','description')


class CustomerForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Cutomer Name ',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))

    short_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Short Name ',
        'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

    }))


    class Meta:

        model = Customer
        fields = ('name','short_name')
    


class ManagerupdateoncallForm(forms.ModelForm):


    class Meta:
        
        model = Profile
        fields =('on_call_person',)

