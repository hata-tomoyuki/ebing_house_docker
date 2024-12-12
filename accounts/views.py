from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm

class SignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    # 自動ログイン 
    def form_valid(self, form):
        # self.object にsave()されたユーザオブジェクトが格納される。
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid

