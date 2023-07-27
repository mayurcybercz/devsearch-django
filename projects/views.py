from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
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
    tags=project.tags.all()
    context={'project':project,'tags':tags}
    return render(request,'projects/single-project.html',context)

@login_required(login_url="login")
def createProject(request):
    profile=request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.owner=profile
            project.save()
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
        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context={'form': form}
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