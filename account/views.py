from django.shortcuts import render
from django.contrib.auth.models import Group, Permission, User
from .models import Account
from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout

# Create your views here.

# def sessioonTest(request):
#     user_id = 

def loginPage(request):
    return render(request, 'account/login.html')

def privatePage(request):
    if request.session.get('user'):
        return render(request, 'account/private.html')
    return render(request, 'account/login.html')

def groupCommunityPage(request):
    return render(request, 'account/groupcommunity.html')

def signUpPage(request):
    return render(request, 'account/signup.html')

def groupPage(request):
    return render(request, 'account/group.html')

def userProfilePage(request):
    return render(request, 'account/userprofile.html')

class CustomLogin(auth_views.LoginView):
    def form_valid(self, form):
        login(self.request, form.get_user())
        # print(form)
        uname = form.get_user()
        print(uname, 'is logined.')
        uesr = User.objects.get(username=uname)
        self.request.session['user'] = uesr.id
        print('session value = ', self.request.session.get('user'))
        return HttpResponseRedirect(self.get_success_url())

class CustomLogout(auth_views.LogoutView):
    def get(self, request, *args, **kwargs):
        if request.session.get('user'):
            print(request)
            del(request.session.get['user'])
        logout(request)
        return HttpResponseRedirect(self.get_success_url_allowed_hosts())


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        # print(request.POST)
        AllUsers = User.objects.all()
        userInfo = request.POST
        print(AllUsers[0].username)
        # if 
    return render(request, 'account/signup.html', {'account': Account})
        # form = UserForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     username = form.cleaned_data.get('username')
        #     raw_password = form.cleaned_data.get('password1')
        #     user = authenticate(username=username, password=raw_password)
        #     login(request, user)
        #     return redirect('index')
#     else:
#         form = UserForm()
#     return render(request, 'common/signup.html', {'form': form})    
# class SignUpView(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         Account(
#             email    = data['email'],
#             password = data['password']
#         ).save()						# 받아온 데이터를 DB에 저장시켜줌

#         return JsonResponse({'message':'회원가입 완료'},status=200)

# class SignInView(View):
#     def post(self, request):
#         data = json.loads(request.body)

#         if Account.objects.filter(email = data['email']).exists() :
#             user = Account.objects.get(email = data['email'])
#             if user.password == data['password'] :
#                 return JsonResponse({'message':f'{user.email}님 로그인 성공!'}, status=200)
#             else :
#                 return JsonResponse({'message':'비밀번호가 틀렸어요'},status = 200)

#         return JsonResponse({'message':'등록되지 않은 이메일 입니다.'},status=200)
 