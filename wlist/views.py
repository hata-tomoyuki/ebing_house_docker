from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from .models import WordsModel, MemoModel, McModel
from .forms import MemoForm, DateRangeForm
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.edit import FormMixin

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from datetime import timedelta
from datetime import date
import random

import logging
logger = logging.getLogger(__name__)

# Create your views here.

# class CustomHomeView(LoginRequiredMixin, TemplateView):
#     template_name = 'home.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['today_date'] = timezone.now().date()
#         return context

class Tutorial(LoginRequiredMixin,TemplateView):
    template_name= 'tutorial.html'


class WordMemoList(LoginRequiredMixin,ListView):
    ## ListViewにより、テンプレート上のobject_listでモデルのインスタンスが渡される。
    template_name = 'list_top.html'
    model = WordsModel
    
    def get_queryset(self):
        return WordsModel.objects.filter(user=self.request.user).order_by('-reg_date','-id')

    def get_context_data(self, **kwargs):
        context = super(ListView,self).get_context_data(**kwargs)
        context['memo_list'] = MemoModel.objects.filter(user=self.request.user).order_by('-reg_date','-id')
        return context

class WordsList(LoginRequiredMixin,ListView):
    template_name = 'list_word.html'
    model = WordsModel
    
    def get_queryset(self):
        return WordsModel.objects.filter(user=self.request.user).order_by('-reg_date','-id')
    
class MemoList(LoginRequiredMixin,ListView):
    template_name = 'list_memo.html'
    model = MemoModel
    
    def get_queryset(self):
        return MemoModel.objects.filter(user=self.request.user).order_by('-reg_date','-id')

class McList(LoginRequiredMixin,ListView):
    template_name = 'mc/list_mc.html'
    model = McModel
    
    def get_queryset(self):
        return McModel.objects.filter(user=self.request.user).order_by('-reg_date','-id')

# class TodoDetail(DetailView):
#     template_name = 'detail.html'
#     model = WordsModel

# class WordsCreate(LoginRequiredMixin,CreateView):
#     template_name = 'word_create.html'
#     model = WordsModel
#     # fields = ('word',)
#     success_url = reverse_lazy('wlist:list_word')  # reverse_lazyは、データが保存された後に実行される。
    
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

class WordsCheck(LoginRequiredMixin,UpdateView):
    template_name = 'word_check.html'
    model = WordsModel
    fields = ('user','word','reg_date','fusen')
    success_url = reverse_lazy('wlist:list_word')
    
class WordsDelete(LoginRequiredMixin,DeleteView):
    template_name = 'word_delete.html'
    model = WordsModel
    success_url = reverse_lazy('wlist:list_word')
    
class WordsUpdate(LoginRequiredMixin,UpdateView):
    template_name = 'word_update.html'
    model = WordsModel
    fields = ('user','word','mean1','mean2','reg_date','fusen')
    success_url = reverse_lazy('wlist:list_word')

    def form_valid(self, form):
        # ラジオボタンで送られた"True"/"False"をBooleanに変換
        fusen_value = self.request.POST.get('fusen')
        print(fusen_value)
        form.instance.fusen = (fusen_value == 'True')
        print(form.instance.fusen)
        return super().form_valid(form)

    # def form_valid(self, form):
    #     instance = form.save(commit=False)
    #     if not instance.reg_date:
    #         instance.reg_date = self.object.reg_date
    #     return super().form_valid(form)

##################################

# class MemoCreate(LoginRequiredMixin,CreateView):
#     template_name = 'memo_create.html' 
#     model = MemoModel
#     form_class = MemoForm
#     success_url = reverse_lazy('wlist:list_memo')  # reverse_lazyは、データが保存された後に実行される。
    
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
    
class MemoDelete(LoginRequiredMixin,DeleteView):
    template_name = 'memo_delete.html' ## wordと同じHTMLファイル
    model = MemoModel
    success_url = reverse_lazy('wlist:list_memo')
    
class MemoUpdate(LoginRequiredMixin,UpdateView):
    template_name = 'memo_update.html'
    model = MemoModel
    fields = ('user','memo','reg_date')
    success_url = reverse_lazy('wlist:list_memo')

###############################################################
# class McCreate(LoginRequiredMixin,CreateView):
#     template_name = 'mc/mc_create.html'
#     model = McModel
#     form_class = MemoForm
#     success_url = reverse_lazy('wlist:list_mc')  # reverse_lazyは、データが保存された後に実行される。
    
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)    
    
class McDelete(LoginRequiredMixin,DeleteView):
    template_name = 'mc/mc_delete.html'
    model = McModel
    success_url = reverse_lazy('wlist:list_mc')
    
class McUpdate(LoginRequiredMixin,UpdateView):
    template_name = 'mc/mc_update.html'
    model = McModel
    fields = ('user','memo1','memo2','reg_date')
    success_url = reverse_lazy('wlist:list_mc')



#######################################################

class BaseRecordView(LoginRequiredMixin, CreateView, ListView):
    template_name = None
    model = None
    fields = None
    success_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localtime(timezone.now())
        context['object_list'] = self.model.objects.filter(
            user=self.request.user,
            reg_date=today.date()
        )        
        # context['today_records'] = self.model.objects.filter(
        #     user=self.request.user,
        #     reg_date=today.date()
        # )
        context['form'] = self.get_form()
        
        return context    
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
        # return super().form_invalid(form)

class McRecord(BaseRecordView):
    template_name = 'mc/mc_record.html'
    model = McModel
    fields = ('memo1', 'memo2',)
    success_url = reverse_lazy('wlist:mc_record')

class WordsRecord(BaseRecordView):
    template_name = 'word_record.html'
    model = WordsModel
    fields = ('word',) 
    success_url = reverse_lazy('wlist:word_record')

class MemoRecord(BaseRecordView):
    template_name = 'memo_record.html'
    model = MemoModel
    fields = ('memo',)
    success_url = reverse_lazy('wlist:memo_record')  

#######################################################
class BaseReview(LoginRequiredMixin, ListView):
    template_name = None
    model = None
    success_url = None 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localtime(timezone.now())        
        context['today_records'] = self.model.objects.filter(
            user=self.request.user, 
            reg_date=today.date())
        
        day_list = [1,7,28]
        passed_list = []
        for i in day_list:            
            passed_list += list(self.model.objects.filter(
                user=self.request.user,
                reg_date=today.date()- timedelta(days=i)))
        
        random.shuffle(passed_list)
        context['passed_records'] = passed_list
        
        return context

class WordsReview(BaseReview):
    template_name = 'word_review.html'
    model = WordsModel
    success_url = reverse_lazy('wlist:word_review')

class MemoReview(BaseReview):
    template_name = 'memo_review.html'
    model = MemoModel
    success_url = reverse_lazy('wlist:memo_review')

class McReview(BaseReview):
    template_name = 'mc/mc_review.html'
    model = McModel
    success_url = reverse_lazy('wlist:mc_review')

#######################################################
class BaseDrill(LoginRequiredMixin, ListView):
    template_name = None
    model = None
    context_object_name = 'drill_records'
    success_url = None
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        form = DateRangeForm(self.request.GET or None)  # GETリクエストからフォームデータを取得
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            drill_list = list(self.model.objects.filter(user=self.request.user,
                                             reg_date__range=(start_date, end_date)))
            random.shuffle(drill_list)
            context['drill_records'] = drill_list
        return context

class WordsDrill(BaseDrill):
    template_name = 'word_drill.html'
    model = WordsModel
    success_url = reverse_lazy('wlist:word_drill')

class WordsCheckDrill(BaseDrill):
    template_name = 'word_check_drill.html'
    model = WordsModel
    success_url = reverse_lazy('wlist:word_check_drill')
    
    def get_context_data(self, **kwargs):
        # BaseDrillから再オーバーライド
        context = super().get_context_data(**kwargs)
        # form = DateRangeForm(self.request.GET or None)  # GETリクエストからフォームデータを取得
        # if form.is_valid():
        drill_list = list(self.model.objects.filter(user=self.request.user,
                                fusen=True))
        random.shuffle(drill_list)
        context['drill_records'] = drill_list
        return context
    
class WordsAll(BaseDrill):
    template_name = 'word_all.html'
    model = WordsModel
    success_url = reverse_lazy('wlist:word_all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_list = list(self.model.objects.filter(user=self.request.user))
        random.shuffle(all_list)
        context['all_records'] = all_list
        return context


class MemoDrill(BaseDrill):    
    template_name = 'memo_drill.html'
    model = MemoModel
    # context_object_name = 'drill_records'
    success_url = reverse_lazy('wlist:memo_drill')

class McDrill(BaseDrill):    
    template_name = 'mc/mc_drill.html'
    model = McModel
    # context_object_name = 'drill_records'
    success_url = reverse_lazy('wlist:mc_drill')
    
class McAll(BaseDrill):
    template_name = 'mc/mc_all.html'
    model = McModel
    # # context_object_name = 'drill_records'
    success_url = reverse_lazy('wlist:mc_all')
    is_all = True

###################################################################

@login_required
def send_email_view(request):
    # example_instance = get_object_or_404(WordsModel, user=request.user)
    user_words =  WordsModel.objects.filter(user=request.user)
    subject = 'Your Data from ExampleModel'
    
    message = f'Hello {request.user.username}\n'
    for w in user_words:
        message += f'{w.word}:{w.mean1},{w.mean2}\n' 
    
    from_email = 'hirotrics@gmail.com'
    recipient_list = [request.user.email]
    
    logger.info(f"------Recipient email------: {request.user.email}")

    send_mail(subject, message, from_email, recipient_list)
    
    return render(request, 'email_sent.html')