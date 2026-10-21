"""В'ЮХИ Django: функції, які отримують запит від браузера і повертають сторінку."""
from django.shortcuts import render

from .forms import LoanForm
from .models import LoanApplication
from .ml import predict


def index(request):
    """Сторінка «Перевірити займ»: форма і результат прогнозу."""
    result = None
    details = None
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            try:
                approved, probability, inputs, model_name = predict(form.cleaned_data)
            except FileNotFoundError:
                form.add_error(None, "Не знайдено файл моделі loan_model.joblib. Спочатку запустіть: python train_model.py")
            else:
                application.approved = approved
                application.probability = probability
                application.save()   # записуємо в базу даних для історії
                result = application
                details = {"inputs": inputs, "model_name": model_name}
    else:
        form = LoanForm()
    return render(request, "predictor/index.html", {"form": form, "result": result, "details": details})


def history(request):
    """Сторінка «Історія перевірок»: усі збережені прогнози і коротка статистика."""
    applications = LoanApplication.objects.all()
    total = applications.count()
    approved = applications.filter(approved=True).count()
    stats = {"total": total, "approved": approved, "rejected": total - approved}
    return render(request, "predictor/history.html", {"applications": applications, "stats": stats})


def about(request):
    """Сторінка «Як це працює»: опис сервісу, технологій та обмежень."""
    return render(request, "predictor/about.html")
