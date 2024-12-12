from django.contrib import admin
from django.urls import path,include
from .views import WordsList, MemoList, WordMemoList, McList,\
WordsDelete, WordsUpdate,WordsRecord, WordsReview, WordsCheckDrill, WordsAll,\
MemoDelete, MemoUpdate,  MemoRecord, MemoReview,\
McDelete, McUpdate, McRecord, McReview,\
WordsDrill, WordsCheckDrill, MemoDrill, McDrill, McAll, Tutorial, send_email_view



app_name = 'wlist'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('tutorial/', Tutorial.as_view(), name='tutorial'),
    path('list_top/', WordMemoList.as_view(), name='list_top'),  ## ？不使用？
    # path('detail/<int:pk>', TodoDetail.as_view(), name='detail'),
    
    # path('word_create/', WordsCreate.as_view(), name='create'),
    path('word_delete/<int:pk>', WordsDelete.as_view(), name='word_delete'),
    path('word_update/<int:pk>', WordsUpdate.as_view(), name='word_update'),
    path('word_record/', WordsRecord.as_view(), name='word_record'),
    path('word_review/', WordsReview.as_view(), name='word_review'),
    # path('word_check/', WordsCheck.as_view(), name='word_check'),
    
    path('word_drill/', WordsDrill.as_view(), name='word_drill'),
    path('word_check_drill', WordsCheckDrill.as_view(), name='word_check_drill'),
    path('word_all', WordsAll.as_view(), name='word_all'),

    path('memo_drill/', MemoDrill.as_view(), name='memo_drill'),
    path('mc/mc_drill/', McDrill.as_view(), name='mc_drill'),
    path('mc/mc_all/', McAll.as_view(), name='mc_all'),
    
    path('memo_record/', MemoRecord.as_view(), name='memo_record'),
    path('memo_review/', MemoReview.as_view(), name='memo_review'),    
    # path('memo_create/', MemoCreate.as_view(), name='memo_create'),
    path('memo_delete/<int:pk>', MemoDelete.as_view(), name='memo_delete'),
    path('memo_update/<int:pk>', MemoUpdate.as_view(), name='memo_update'),

    path('mc/mc_record/', McRecord.as_view(), name='mc_record'),
    path('mc/mc_review/', McReview.as_view(), name='mc_review'),    
    # path('mc/mc_create/', McCreate.as_view(), name='mc_create'),
    path('mc/mc_delete/<int:pk>', McDelete.as_view(), name='mc_delete'),
    path('mc/mc_update/<int:pk>', McUpdate.as_view(), name='mc_update'),

    path('list_word/', WordsList.as_view(), name='list_word'),
    path('list_memo/', MemoList.as_view(), name='list_memo'),
    path('mc/list_mc/', McList.as_view(), name='list_mc'),
    
    #不使用
    path('send_email/', send_email_view, name='send_email'),
]

