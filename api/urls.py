from django.urls import path
from .views import signup, login, mark_as_spam, unmark_as_spam

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('mark_as_spam/', mark_as_spam, name='mark_as_spam'),
    path('unmark_as_spam/', unmark_as_spam, name='unmark_as_spam')
]
