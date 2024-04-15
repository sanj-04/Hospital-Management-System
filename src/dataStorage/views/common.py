# from django.http import HttpResponseRedirect
# from django.urls import reverse

# def login_required_tm(func):
#     def wrapper(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             HttpResponseRedirect(reverse('dataStorage:doctor_home'), status=301)
#         return func(request, *args, **kwargs)
#     return wrapper
