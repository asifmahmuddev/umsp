from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Student, Faculty
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, ListView
from .forms import StudentSignUpForm, FacultySignUpForm, DeptForm, CreateCourseForm, CreateSemesterForm, AssignCourseForm
from advising.models import Department, Course, Create_Semester, AssignedCourse, TakeCourse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import date, datetime



def Homepage(request):
    return render(request, 'home/homepage.html')


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'home/student_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Successfully SignUp')
        return redirect('student_signup')


def StudentListView(request):
    student = Student.objects.all();

    return render(request, 'home/student_list.html', {'std': student});


class FacultySignUpView(CreateView):
    model = User
    form_class = FacultySignUpForm
    template_name = 'home/faculty_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'faculty'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Successfully SignUp')
        return redirect('faculty_signup')


def FacultyListView(request):
    faculty = Faculty.objects.all();

    return render(request, 'home/faculty_list.html', {'fac': faculty});


def DepartmentListView(request):
    department = Department.objects.all();

    return render(request, 'home/department_list.html', {'dep': department});


def SemesterListView(request):
    semester = Create_Semester.objects.all();

    return render(request, 'home/semester_list.html', {'sem': semester});


def CourseListView(request):
    course = Course.objects.all();

    return render(request, 'home/course_list.html', {'cou': course});


def AssignedCourseListView(request):
    assigned_course = AssignedCourse.objects.all();

    return render(request, 'home/assigned_course_list.html', {'ass': assigned_course});


@login_required
def Profile(request):
    student = Student.objects.filter(user=request.user)
    faculty = Faculty.objects.filter(user=request.user)
    #print(faculty)

    context = {
        'student': student,
        'faculty': faculty
    }
    return render(request, 'home/profile.html', context)


def DeptView(request):
    form = DeptForm
    if request.method == 'POST':
        deptform = DeptForm(request.POST)
        #print(deptform)

        if deptform.is_valid():
            deptform.save()
            messages.success(request, 'Successfully Submitted')
            return redirect('department')
        else:
            messages.error(request, 'Error! Department Already Assigned.')
            return redirect('department')

    return render(request, 'home/department.html', {'form': form})


def CreateSemesterView(request):
    form = CreateSemesterForm
    if request.method == 'POST':
        semesterform = CreateSemesterForm(request.POST)

        if semesterform.is_valid():
            semesterform.save()
            messages.success(request, 'Successfully Submitted')
            return redirect('create_semester')
        else:
            messages.error(request, 'Error! Semester Already Assigned.')
            return redirect('create_semester')

    return render(request, 'home/create_semester.html', {'form': form})


class CreateCourseView(CreateView):
    model = Course
    form_class = CreateCourseForm
    template_name = 'home/create_course.html'

    def form_valid(self, form):
        if self.request.method == 'POST':
            courseform = CreateCourseForm(self.request.POST)

            if courseform.is_valid():
                if 1 <= float(courseform.cleaned_data['credit']) <= 4.5:
                    courseform.save()
                    messages.success(self.request, 'Successfully Submitted')
                    return redirect('register_course')
                else:
                    messages.error(self.request, 'Invalid! Credit')
                    return redirect('register_course')

def AssignCourseView(request):
    form = AssignCourseForm
    if request.method == 'POST':
        assignform = AssignCourseForm(request.POST)

        if assignform.is_valid():
            courses = Course.objects.all()
            course = assignform.cleaned_data["course"]
            has_lab = assignform.cleaned_data["has_lab"]
            lab_weekday = assignform.cleaned_data["l_Time_WeekDay"]
            lab_room = assignform.cleaned_data["l_Room"]
            for c in courses:
                if c == course and float(c.credit) == 3:
                    if has_lab or lab_weekday or lab_room:
                        messages.error(request, 'Invalid! The chosen course does not fulfill all of the lab requirements.')
                        return redirect('assign_course')

            assignform.save()
            messages.success(request, 'Successfully Submitted')
            return redirect('assign_course')

    return render(request, 'home/assign_course.html', {'form': form})


@csrf_exempt
def Schedule(request):
    semester = Create_Semester.objects.values()

    obj = {
        'semesters': semester,
        'courses': 'Null'
    }
    if request.method=='POST':
        s = request.POST['semester']

        course = (TakeCourse.objects.filter(student_info=request.user.id, current_semester=s))

        obj = {
        'semesters': semester,
        'courses': course
        }
    return render(request, 'home/class_schedule.html', obj)



@csrf_exempt
def drop_course(request):
    user = User.objects.filter(is_student=True)
    semester = Create_Semester.objects.values()
    current_s = Create_Semester.objects.all()
    s = []
    if current_s:
        s = current_s[len(current_s) - 1]
    taken =""

    context = {
        'user': user,
        'semester': semester,
        
        'add': 'Null',
        'taken':'Null'

    }

    #print(user)

    if request.method == 'POST':
        
        stu = request.POST['user1']
        #print(stu)
        add=""

        #st = User.objects.get(username=stu)
        # add = AssignedCourse.objects.filter(current_semester=s)
        previous_taken = TakeCourse.objects.filter(~Q(current_semester__contains=s))
        student = Student.objects.get(user=stu)
        taken = TakeCourse.objects.filter(Q(current_semester__contains=s))
        student=str(student)
        context = {
            'user': user,
            'semester': semester,
            'previous_taken': previous_taken,
            'student': student,
            'add': add,
            'taken': taken,
            'stuId':stu

        }
    return render(request,'home/drop_course.html',context)


@csrf_exempt
def drop(request):
    if request.method=='POST':
        detail = request.POST['details']
        details = detail.split(",")
        
        dat = TakeCourse.objects.get(course=details[0], section=details[1], student_info=details[4])
        dat.withdraw_status=True
        dat.save()
        return JsonResponse({"status":200})


def Grade_Report(request):
    taken=TakeCourse.objects.filter(student_info=request.user)
    course_list=[]
    for x in taken:
        course_list.append(x.course)  #CSE103 , GEN201
    course=Course.objects.filter(course_code__in=course_list)
    detail={}
    grade_c = {"A+":4,"A":4,"A-":3.7,"B+":3.30,"B":3.0,"B-":2.67, "C+":2.33,"C":2.0,"C-":1.67,"D+":1.33,"D":1.0,"F":0,'Did not assign':-1}
    sum=0
    count=0
    for x in taken:
        for y in course:
            if y.course_code == x.course:
                list1=[]
                list1.append(x.course)
                list1.append(y.course_title)
                list1.append(y.credit)
                list1.append(x.grade)
                
                sum+=grade_c[x.grade]
                list1.append(x.current_semester)
                detail[x.course]=list1
    semester_set=[]
    
    
    # getting unique semesters
    for x in taken:
        semester_set.append(x.current_semester)
    semester_set=set(semester_set)
    
    sum=0
    count=0
    sem_cg={}
    credit=0
    for sem in semester_set:
        sum=0
        credit=0
        for x in taken:
            for y in course:
                if y.course_code == x.course and sem == x.current_semester:
                    sum+=grade_c[x.grade]*x.credit
                    credit+=x.credit
        sem_cg[sem]= {"semester":sem,"cg":round(sum / credit,2)}
    
    
    d = datetime.now().strftime("%d %b, %Y")
    
    obj={
        "date":d,
        'detail':detail,
        "semesters":semester_set,
        "user":request.user,
        "courses":taken,
        "course_detail":course,
        "semester_cg":sem_cg.values()
    }
    return render(request,'home/grade_report.html',obj)
