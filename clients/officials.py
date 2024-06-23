from django.shortcuts import render
# صفحة الفيو للمسؤولين

def index(request):
    return render(request , 'officials/dashboard.html')

# # Create your views here.
# def login_backend(request):
#     return render(request , 'login.html')

# # Create your views here.
# def forget_password(request):
#     return render(request , 'forget_password.html')


# # Create your views here.
# def branches(request):
#     return render(request , 'branshes.html')

# # Create your views here.
def report_table(request):
    return render(request , 'officials/report-table.html')

# # Create your views here.
def report(request):
    return render(request , 'officials/report.html')

# # Create your views here.
# def profile(request):
#     return render(request , 'profile.html')

# # Create your views here.
def queries(request):
    return render(request , 'officials/queries.html')

# # Create your views here.
# def officials_queries(request):
#     return render(request , 'officials_queries.html') 

# # Create your views here.
# def contactus(request):
#     return render(request , 'pages-contact-us.html')

# # Create your views here.
# def pagefaq(request):
#     return render(request , 'page-faq.html')