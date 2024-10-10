from django.shortcuts import render,redirect

# Create your views here.

from django.views.generic import View

from notesworks.forms import TaskForm , RegistrationForm , SignInForm

from django.contrib import messages

from notesworks.models import Task

from django import forms

from django.db.models import Q

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from notesworks.decorators import sigin_required

from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache

from django.db.models import Count

decs=[sigin_required,never_cache]

@method_decorator(decs,name="dispatch")

class TaskCreateView(View):

    def get(self,request,*args,**kwargs):


        form_instance=TaskForm()


        return render(request,"task_create.html",{"form":form_instance})
    
    
    def post(self,request,*args,**kwargs):


        form_instance=TaskForm(request.POST)


        if form_instance.is_valid():
           

           form_instance.instance.user=request.user
           

           form_instance.save()


           messages.success(request,"task created sucessfully")


           return redirect("task-list")
        
        else:

            messages.error(request,"task is failed")


            return render(request,"task_create.html",{"form":form_instance})
        
@method_decorator(decs,name="dispatch")  

class TaskListView(View):

    def get(self,request,*args,**kwargs):
            
            
            search_text=request.GET.get("search_text")
            
            selected_category=request.GET.get("category","all")

            if selected_category == "all":

                qs=Task.objects.filter(user=request.user)

            else:

                qs=Task.objects.filter(category=selected_category,user=request.user)

            if search_text!=None:
                qs=Task.objects.filter(user=request.user)
                qs=qs.filter(Q(title__icontains=search_text)|Q(description__icontains=search_text))

            return render(request,"task_list.html",{"tasks":qs,"selected":selected_category})

@method_decorator(decs,name="dispatch")   

class TaskDetailView(View):

    def get(self,request,*args,**kwargs):

        #eaxtract from id from url

        id=kwargs.get("pk")

        #fecthing task with id

        qs=Task.objects.get(id=id)

        return render(request,"task_detail.html",{"task":qs})
    
@method_decorator(decs,name="dispatch")
    
class TaskUpdateView(View):

    def get(self,request,*args,**kwargs):

        #extract pk from kwargs
        id=kwargs.get("pk")

        #fetch task object with id =id
        task_obj=Task.objects.get(id=id)

        #intialize taskform with tASK_OBJ
        form_instance=TaskForm(instance=task_obj)

        #adding status feild to form_instance
        form_instance.fields["status"]=forms.ChoiceField(choices=Task.status_choices,widget=forms.Select(attrs={"class":"form-control form-select"}),initial=task_obj.status)

        return render(request,"task_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        #extreact id from kwargs
        id=kwargs.get("pk")

        #fetch task object with id
        task_obj=Task.objects.get(id=id)

        #initialize from with request.POST and instance
        form_instance=TaskForm(request.POST,instance=task_obj)


        #CHK FORM IS VALID for error checking
        if form_instance.is_valid():
           

            #add status to forms instance
           form_instance.instance.status=request.POST.get("status")

          #save form_instance
           form_instance.save() 

           return redirect("task-list")
        
        else:

           return render(request,"task_edit.html",{"form":form_instance})
        
@method_decorator(decs,name="dispatch")

class TaskDeleteView(View):

    def get(self,request,*args,**kwargs):

        #extract id and delkete task object with this id
        Task.objects.get(id=kwargs.get("pk")).delete()

        return redirect("task-list")
    

from django.db.models import Count

@method_decorator(decs,name="dispatch")
    
class TaskSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Task.objects.filter(user=request.user)

        total_task_count=qs.count()

        category_summary=qs.values("category").annotate(cat_count=Count("category"))
        print(category_summary)

        status_summary=qs.values("status").annotate(stat_count=Count("status"))
        print(status_summary)


        context={

                  "total_task_count":total_task_count,

                  "category_summary":category_summary,

                  "status_summary":status_summary,
                    
        }

        return render(request,"dash_board.html",context)
    
class SignupView(View):

    template_name="register.html"

    def get(self,request,*args,**kwargs):

        from_instance=RegistrationForm()
    
        return render(request,self.template_name,{"form":from_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            return redirect("signin")
        
        else:

         return render(request,self.template_name,{"form":form_instance})
        

class SignInView(View):


    template_name="login.html"


    def get(self,request,*args,**kwargs):


        form_instance=SignInForm()


        return render(request,self.template_name,{"form":form_instance})
    
    
    def post(self,request,*args,**kwargs):


        form_instance=SignInForm(request.POST)


        if form_instance.is_valid():


            username=form_instance.cleaned_data.get('username')


            password=form_instance.cleaned_data.get('password')


            user_object=authenticate(request,username=username,password=password)


            if user_object:


                login(request,user_object)


                return redirect("task-list")
            
            
        return render(request,self.template_name,{"form":form_instance})
    
@method_decorator(decs,name="dispatch")

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('signin')
    
class DashBoardView(View):

    template_name="dash_board.html"

    def get(self,request,*args,**Kwargs):

        return render(request,self.template_name)

        



        

       






    
    
     


       












        


