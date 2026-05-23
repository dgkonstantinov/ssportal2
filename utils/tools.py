# -*- coding: utf-8 -*-
from slugify import slugify  # python-slugify


# import os
# import re
# from django.conf import settings
# from django.shortcuts import redirect
# from django.http import HttpResponse, Http404
# import datetime
# from django.utils import timezone


def create_slug(value: str):
    if value.count('.'):
        value = value.strip('.')
        value = value[0]
    return slugify(value)

# def is_ip_address(value):
#     try:
#         octets = value.split(".")
#         for octet in octets:
#             if octet.isdigit():
#                 if not (1 <= int(octet) <= 255):
#                     return False
#             else:
#                 return False
#         return True
#     except:
#         return False
#
#
# def upload_file_for_equipment(instance, file_name):
#     equipment_directory = "equipments"
#     sub_directory = str(instance.__class__.__name__).lower()
#     upload_directory = f"{equipment_directory}/{sub_directory}/{str(instance.sn).lower()}"
#     if not os.path.exists(upload_directory):
#         os.makedirs(upload_directory)
#
#     file_name, file_extension = os.path.splitext(os.path.split(file_name)[1])
#     file_name = f"{create_slug(file_name.replace('.', '-'))}{file_extension}"
#
#     return os.path.join(upload_directory, file_name)
#
#
# def download_file(request):
#     if request.GET.get("file"):
#         file = f"{settings.MEDIA_ROOT}/{request.GET['file']}"
#
#         if os.path.exists(file):
#             with open(file, 'rb') as fh:
#                 response = HttpResponse(fh.read(), content_type="application/data")
#                 response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file)
#                 return response
#     raise Http404
#
#
# def delete_file(request):
#     from settings.models import Tasks, TaskTypes, TaskStatus
#     from support.models import SupportCases
#     from servers.models import Servers
#
#     if request.GET.get("file"):
#         file = f"{settings.MEDIA_ROOT}/{request.GET['file']}"
#         if os.path.exists(file):
#             os.remove(file)
#
#     if request.POST:
#         if (request.POST.get("file")
#                 and request.POST.get("file_name")
#                 and request.POST.get("case_id")):
#             case = SupportCases.objects.get(pk=request.POST.get("case_id"))
#             file = f"{settings.MEDIA_ROOT}/{request.POST['file']}"
#             if os.path.exists(file):
#                 os.remove(file)
#                 task_name = f"Delete file in case: {case.number}"
#                 description = (f"Delete file: {request.POST.get('file_name')}\n"
#                                f"Case number: {case.number}\n"
#                                f"Case name: {case.name}\n"
#                                f"User: {request.POST.get('user')}\n"
#                                f"Path: {request.POST.get('file')}\n")
#
#                 Tasks.objects.create(name=task_name, task_type=TaskTypes.objects.get(slug='portal'),
#                                      task_status=TaskStatus.objects.get(slug='successful'),
#                                      description=description, end=timezone.make_aware(datetime.datetime.now()))
#
#         elif (request.POST.get("file")
#               and request.POST.get("file_name")
#               and request.POST.get("server_id")):
#             server = Servers.objects.get(pk=request.POST.get("server_id"))
#             file = f"{settings.MEDIA_ROOT}/{request.POST['file']}"
#             if os.path.exists(file):
#                 os.remove(file)
#                 task_name = f"Delete file: server {server.os_name}"
#                 description = (f"Delete file: {request.POST.get('file_name')}\n"
#                                f"Server serial number: {server.sn}\n"
#                                f"User: {request.POST.get('user')}\n"
#                                f"Path: {request.POST.get('file')}\n")
#                 Tasks.objects.create(name=task_name, task_type=TaskTypes.objects.get(slug='portal'),
#                                      task_status=TaskStatus.objects.get(slug='successful'),
#                                      description=description, end=timezone.make_aware(datetime.datetime.now()))
#
#     return redirect(request.META.get('HTTP_REFERER'))
#
#
# def translated_text(value: str = "") -> str:
#     value = value.strip().lower()
#     if re.search(r"[а-яА-Я]", value):
#         cyrillic_to_latin = {
#             "й": "q", "ц": "w", "у": "e", "к": "r", "е": "t", "н": "y", "г": "u", "ш": "i", "щ": "o", "з": "p",
#             "х": "[", "ъ": "]", "ф": "a", "ы": "s", "в": "d", "а": "f", "п": "g", "р": "h", "о": "j", "л": "k",
#             "д": "l", "ж": ";", "э": "'", "я": "z", "ч": "x", "с": "c", "м": "v", "и": "b", "т": "n", "ь": "m",
#             "б": ",", "ю": "."}
#         tr_value = ""
#         for ch in value:
#             if cyrillic_to_latin.get(ch):
#                 tr_value = tr_value + cyrillic_to_latin[ch]
#             else:
#                 tr_value = tr_value + ch
#
#         return tr_value
#     else:
#         return value
