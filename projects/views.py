from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Project,Tag
from .forms import ProjectForm,ReviewForm
from .utils import searchProjects,paginateProjects



def projects(request):
    #search projects
    projects,search_query=searchProjects(request)
    #paginate projects
    custom_range,projects=paginateProjects(request,projects,results=6)
    context={'projects':projects,'search_query':search_query,'custom_range':custom_range}
    return render(request,'projects/projects.html',context)

def project(request,pk):
    project=Project.objects.get(id=pk)
    form=ReviewForm()
    if request.method == 'POST':
        form=ReviewForm(request.POST)
        review=form.save(commit=False)
        review.project=project
        review.owner=request.user.profile
        review.save()
        #update project vote count
        project.getVoteCount
        messages.success(request,"Review added successfully!")
        return redirect('project',pk=project.id)
    
    context={'project':project,'form':form}
    return render(request,'projects/single-project.html',context)

@login_required(login_url="login")
def createProject(request):
    profile=request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        # to handle new form input for tags
        newtags=request.POST.get('newtags').replace(',',' ').split()
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.owner=profile
            project.save()
            for tag in newtags:
                tag,created=Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            form.save_m2m() # save many-to-many data i.e tags
            return redirect('account')
    context={'form': form}
    return render(request,'projects/project_form.html',context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        # to handle tags in new form field
        newtags=request.POST.get('newtags').replace(',',' ').split()

        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            for tag in newtags:
                tag,created=Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
        #need to pass project in context for js eventlistener to make changes
    context={'form': form,'project':project}
    return render(request,'projects/project_form.html',context)

@login_required(login_url="login")
def deleteProject(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return  redirect('account')
    context={'object': project}
    return render(request,'delete_template.html',context)