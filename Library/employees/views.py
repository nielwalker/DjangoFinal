from django.shortcuts import render
import csv
from .models import Post
# Create your views here.


def emp_view(request):
    return render(request, 'First.html')

def emp_entry(request):
    if request.method=='POST':
        employee_dict=request.POST
        with open('employee.csv', 'a') as bk:
            W=csv.writer(bk)
            for key,value in employee_dict.items():
                W.writerow([key,value])
    return render(request, 'employeedetail.html')

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts':posts})
