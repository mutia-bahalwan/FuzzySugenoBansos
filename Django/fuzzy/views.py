from django.shortcuts import render
from fuzzy.sugeno import sugeno

def home(request):
    if request.method == "POST":
        ability = float(request.POST.get("ability"))
        dp = float(request.POST.get("dp"))
        work = float(request.POST.get("work"))
        guarantee = float(request.POST.get("guarantee"))

        result = sugeno(ability, dp, work, guarantee)

        decision = "ACCEPT" if result >= 150 else "REJECT"
        suggestion = "Direkomendasikan diterima." if result >= 150 else "Sebaiknya ditolak."

        return render(
            request,
            "fuzzy/home.html",
            {
                "result": result,
                "decision": decision,
                "suggestion": suggestion
            }
        )

    return render(request, "fuzzy/home.html")

def result(request):
    income = float(request.POST['income'])
    family = float(request.POST['family'])
    house  = float(request.POST['house'])

    data = sugeno(income, family, house)  

    return render(request, "fuzzy/result.html", {
        "data": data, 
    })

