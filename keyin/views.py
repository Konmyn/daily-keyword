from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
from datetime import datetime
from collections import defaultdict
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

import io
import base64

from .forms import KeyForm
from .helper import get_word_cloud_by_freq


# 每日关键词输入
def keyin(request):
    print(request.user)
    # print(request.build_absolute_uri())  # http://localhost:8000/inputf/
    # print(request.META['PATH_INFO'])  # /inputf/
    # print(reverse("input-simple"))
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = KeyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # print(form.cleaned_data)
            # print(type(form.cleaned_data)) # dict
            df = pd.read_csv("key_info.csv", index_col=0, dtype=str)
            new = pd.DataFrame(form.cleaned_data, index=[datetime.now().strftime("%Y-%m-%d")])
            df = df.append(new)
            df.to_csv("key_info.csv")
            return HttpResponseRedirect(reverse("info"))

    # if a GET (or any other method) we'll create a blank form
    else:
        df = pd.read_csv("key_info.csv", index_col=0, dtype=str)
        if datetime.now().strftime("%Y-%m-%d") in df.index:
            return HttpResponseRedirect(reverse("info"))
        # print(df.loc["2019-07-02"])
        # print(df.info())
        form = KeyForm(request=request)
    # https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
    return render(request, 'keyin.html', {'form': form})


# 关键词综合信息展示
def info(request):
    print(request.user)
    df = pd.read_csv("key_info.csv", index_col=0, dtype=str)
    return HttpResponse(df.to_html())


# 关键词词云
def cloud(request):
    print(request.user)
    df = pd.read_csv("key_info.csv", index_col=0, dtype=str)
    freq = defaultdict(int)
    for index, row in df.iterrows():
        if row["primary_key"]:
            freq[row["primary_key"]] += 8
        if row["secondary_key"]:
            freq[row["secondary_key"]] += 4
        if row["ternary_key"]:
            freq[row["ternary_key"]] += 2
        if row["quartus_key"]:
            freq[row["quartus_key"]] += 1
        if row["fifth_key"]:
            freq[row["fifth_key"]] += 1
    # print(freq)
    wc = get_word_cloud_by_freq(freq)
    image = wc.to_image()
    # print(dir(image))
    # image.show()  # can work
    # response = HttpResponse(content_type="image/png")
    # image.save(response, "PNG")
    # return response
    cio = io.BytesIO()
    image.save(cio, "PNG")
    bdata = base64.b64encode(cio.getvalue()).decode("ascii")
    image_data = "data:image/png;base64,{}".format(bdata)
    return render(request, 'image.html', {"image_data": image_data})


# 起始页面
def start(request):
    print(request.user)
    return render(request, 'start.html')


# 登录页面
def userlogin(request):
    print(request.user)
    if not request.user.is_anonymous:
        return HttpResponseRedirect(reverse("start"))
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("start"))
    return render(request, 'login.html')


# 登录页面
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse("start"))