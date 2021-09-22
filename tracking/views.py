import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import (DeleteCateogryForm, DeleteTrackableForm, EditCategoryForm,
                    EditTrackableForm, NewCategoryForm, NewTrackableForm)
from .models import Category, Cycle, Day, Trackable


############# NOT VIEWS ###############
def create_cycle(date, dayobj):
    id = Cycle.objects.count()
    Cycle.objects.create(idnum=id + 1, first=date)  # making new cycle
    dayobj.cycle = Cycle.objects.get(idnum=id + 1)  # adding new cycle to day object
    dayobj.save()

    # if this is not the first cycle to be created....
    if id > 0:
        a = Cycle.objects.get(idnum=id)
        a.last = date - datetime.timedelta(1)  # ending last cycle
        a.save()

        a.duration = (a.last - a.first).days  # setting last cycle duration
        a.save()
    return


def date_convert(
    strdate,
):  ####### To add string dates from postman. could also use datetime.strptime
    lst = strdate.split("/")
    newdate = datetime.date(int(lst[0]), int(lst[1]), int(lst[2]))
    return newdate


def list_all():
    days = []
    cycles = []
    trackables = []

    for day in Day.objects.all():
        log = []
        for i in day.logs.all():
            log.append(i.name)

        days.append([day.date, log, f"cycle begin date: {day.cycle}"])

    for trackable in Trackable.objects.all():
        trackables.append(trackable.name)

    for cycle in Cycle.objects.all():
        cycles.append([cycle.first, cycle.last])

    return f"days: {days} <br> cycles: {cycles} <br> trackables: {trackables}"
    # return output


########################################


@csrf_exempt
def tracking(request):
    if request.method == "POST":
        try:
            thisdate = date_convert(request.POST.get("date"))  ##convert is for postman
            thislog = request.POST.get("log").split(", ")

            try:
                a = Day.objects.get(date=thisdate)
            except:
                Day.objects.create(date=thisdate)

            for log in thislog:
                Day.objects.get(date=thisdate).logs.add(Trackable.objects.get(name=log))

            cnt = 0
            if "blood" in thislog:
                for day in Day.objects.filter(
                    date__gt=thisdate - datetime.timedelta(10)
                ):
                    if Trackable.objects.get(name="blood") in day.logs.all():
                        cnt += 1
                if 0 == 0:
                    create_cycle(thisdate, Day.objects.get(date=thisdate))

            return HttpResponse(f"<b> Successfully Saved!</b><br><br>{list_all()}")
        except Exception as e:
            return HttpResponse(
                f"<b> Sorry, there was an error. Your entry was not saved. </br> here's the error: <hr> {e.args} <hr>"
            )
    if request.method == "GET":
        return HttpResponse("Hi. To use stuff, send a post request.📧")


@csrf_exempt
def add_cycle(request):
    if request.method == "POST":
        thisdate = date_convert(request.POST.get("date"))  ##convert is for postman
        id = Cycle.objects.count() + 1
        Cycle.objects.create(idnum=id, first=thisdate, last=thisdate)
        Cycle.objects.create(idnum=id + 1, first=thisdate)
        a = Cycle.objects.get(idnum=id + 1)
        a.last = thisdate
        a.save()

        return HttpResponse(Cycle.objects.values())


def database(request):
    return HttpResponse(
        f"<h1> Days</h1> {list(Day.objects.all().values())} <h1> Cycles</h1> {list(Cycle.objects.all().values())} <h1> Trackables </h1> {list(Trackable.objects.all().values())}<h1> Categories </h1> {list(Category.objects.all().values())}"
    )


@csrf_exempt
def trackable_manage(request):
    relateddict = dict()
    for cat in Category.objects.all():
        relateddict[cat.name] = cat.trackable_set.all()

    forms = {
        "newcat": NewCategoryForm(),
        "newtrack": NewTrackableForm(),
        "editcat": EditCategoryForm(),
        "edittrack": EditTrackableForm(),
        "deletecat": DeleteCateogryForm(),
        "deletetrack": DeleteTrackableForm(),
    }

    if request.method == "GET":
        return render(
            request,
            "trackables.html",
            context={"catdict": relateddict, "done": "", "forms": forms},
        )

    if request.method == "POST":
        if "addcategory" in request.POST:
            form = NewCategoryForm(request.POST)
            if form.is_valid():
                Category.objects.create(name=form.cleaned_data["name"])
        elif "addtrackable" in request.POST:
            form = NewTrackableForm(request.POST)
            if form.is_valid():
                cat = Category.objects.get(name=form.cleaned_data["category"])
                Trackable.objects.create(
                    name=form.cleaned_data["name"], category_id=cat.id
                )
        elif "editcategory" in request.POST:
            form = EditCategoryForm(request.POST)
            if form.is_valid():
                cat = Category.objects.get(name=form.cleaned_data["name"])
                cat.name = form.cleaned_data["newname"]
                cat.save()
        elif "deletecategory" in request.POST:
            form = DeleteCateogryForm(request.POST)
            if form.is_valid():
                Category.objects.get(name=form.cleaned_data["name"]).delete()
        elif "edittrackable" in request.POST:
            form = EditTrackableForm(request.POST)
            if form.is_valid():
                track = Trackable.objects.get(form.cleaned_data["name"])
                track.name = form.cleaned_data["newname"]
                track.category_id = form.cleaned_data["newcat"]
        elif "deletetrackable" in request.POST:
            form = EditTrackableForm(request.POST)
            if form.is_valid():
                Trackable.objects.get(name=form.cleaned_data["name"]).delete()

        return render(
            request,
            "trackables.html",
            context={"catdict": relateddict, "done": "Changes Saved!", "forms": forms},
        )
        task = request.POST.get("task")
        name1 = request.POST.get("name1")

        if task == "add":
            try:
                a = Trackable.objects.get(name=name1)
                return HttpResponse(
                    f"<b>You've already added this trackable!</b><br><br>{list_all()}"
                )
            except:
                Trackable.objects.create(name=name1)
                return HttpResponse(
                    f"<b> {name1} successfully saved!</b><br><br>{list_all()}"
                )
        elif task == "delete":
            try:
                Trackable.objects.get(name=name1).delete()
                return HttpResponse(
                    f"<b> {name1} successfully deleted!</b><br><br>{list_all()}"
                )
            except:
                return HttpResponse(
                    f"<b> Sorry, There is no Trackable with this name. </b><br> Have you typed the name correctly? "
                )
        elif task == "edit":
            try:
                t = Trackable.objects.get(name=name1)
                name2 = request.POST.get("name2")
                try:
                    Trackable.objects.get(name=name2)
                    return HttpResponse(
                        f"<b>Hmmm. {name2} already exists in your Trackables! </b><br><br>{list_all()}"
                    )
                except:
                    t.name = name2
                    t.save()
                    return HttpResponse(
                        f"<b> {name1} successfully Changed to {name2}!</b><br><br>{list_all()}"
                    )
            except:
                return HttpResponse(
                    f"<b> Sorry, There is no Trackable with this name. </b><br> Have you typed the name correctly? "
                )


@csrf_exempt
def add_categories(request):
    if request.method == "POST":
        names = request.POST.get("names").split("\n")
        cats = request.POST.get("cats").split("\n")
        for i in range(len(names)):
            try:
                a = Category.objects.get(name=cats[i])
            except:
                a = Category(name=cats[i])
                a.save()
            thing = Trackable.objects.get(name=names[i])
            thing.category_id = a.id
            thing.save()
        return HttpResponse("done!")

