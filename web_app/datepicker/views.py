from django.shortcuts import render
import json
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from .models import Post
from .models import Dates
import csv

# dummy data to test website
posts = [
    {
        'StationID': 'Station 1',
        'Location': 'Tifton, GA',
        'MonitoringSystem': 'info on Georgia Environmental Monitoring System and whitefly pictures',
        'date_posted': 'date info'
    },
    {
        'StationID': 'Station 2',
        'Location': 'Phillipsburg, GA',
        'MonitoringSystem': 'info on Georgia Environmental Monitoring System and whitefly pictures',
        'date_posted': 'date info'
    }
]


def post(request):
    # context = {
    #     'posts': Post.objects.all()
    #     # 'posts': posts
    # }
    displaypost = Post.objects.all()
    displaydata = Dates.objects.all()
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        searchresult = Dates.objects.raw(
            'Select datepicker_dates.id, datepicker_dates.img1, datepicker_dates.img2 from datepicker_dates inner Join datepicker_post on datepicker_dates.location_id = datepicker_post.id where date_posted between "' + fromdate + '" and "' + todate + '"')
        return render(request, 'datepicker/post.html', {"posts": displaypost, "data": searchresult})
    else:
        displaydata = Dates.objects.all()
        return render(request, 'datepicker/post.html', {"data": displaydata, "posts": displaypost})
    # return render(request, 'datepicker/home.html', context)


# def showresults(request):
#     displaydata = Dates.objects.all()
#     return render(request, 'datepicker/home.html', {"data": displaydata})


def about(request):
    return render(request, 'datepicker/about.html', {'title': 'About'})


def home(request):
    s = 0
    res = Dates.objects.raw(
        'Select * from datepicker_dates inner Join datepicker_post on datepicker_dates.location_id = datepicker_post.id')
    for c in res:
        s += c.count1 + c.count2
    return render(request, 'datepicker/home.html', {'title': 'Map', 'Sum': s})


def stats(request):
    labels = []
    data1 = []
    data2 = []
    dic = {}
    displaypost = Post.objects.all()
    if request.method == "POST":
        fromd = request.POST.get('fromdate')
        tod = request.POST.get('todate')
        result = Dates.objects.raw(
            'Select * from datepicker_dates inner Join datepicker_post on datepicker_dates.location_id = datepicker_post.id where date_posted between "' + fromd + '" and "' + tod + '"')
        for location in result:
            if location.Location not in dic:
                dic[location.Location] = [0, 0]
            if location.Location in dic:
                dic[location.Location][0] += int(location.count1)
                dic[location.Location][1] += int(location.count2)
        for key in dic:
            labels.append(key)
            data1.append(dic[key][0])
            data2.append(dic[key][1])
            # labels.append(location.Location)
            # data.append(location.count1)
        return render(request, 'datepicker/stats.html', {'Location': labels, 'AM': data1, 'PM': data2})
    else:
        res = Dates.objects.raw(
            'Select * from datepicker_dates inner Join datepicker_post on datepicker_dates.location_id = datepicker_post.id')
        for location in res:
            if location.Location not in dic:
                dic[location.Location] = [0, 0]
            if location.Location in dic:
                dic[location.Location][0] += int(location.count1)
                dic[location.Location][1] += int(location.count2)
        for key in dic:
            labels.append(key)
            data1.append(dic[key][0])
            data2.append(dic[key][1])
        return render(request, 'datepicker/stats.html', {
            'Location': labels,
            'AM': data1,
            'PM': data2
        })


def export_csv(request):
    if request.method == "POST":
        fromd = request.POST.get('fromdate')
        tod = request.POST.get('todate')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=whiteflydata.csv'
        writer = csv.writer(response)
        writer.writerow(['Location', 'Date Posted', 'AM', 'PM'])
        data = Dates.objects.raw(
            'Select * from datepicker_dates inner Join datepicker_post on datepicker_dates.location_id = datepicker_post.id where date_posted between "' + fromd + '" and "' + tod + '"')
        for item in data:
            writer.writerow([item.Location, item.date_posted, item.count1, item.count2])

        return (response)
    else:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=whiteflydata.csv'
        writer = csv.writer(response)
        writer.writerow(['Location', 'Date Posted', 'AM', 'PM'])
        data = Dates.objects.raw('Select * from datepicker_dates inner Join datepicker_post on datepicker_dates.location_id = datepicker_post.id')
        for item in data:
            writer.writerow([item.Location, item.date_posted, item.count1, item.count2])

        return response

