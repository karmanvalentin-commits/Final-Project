"""ФОРМИ Django: автоматично створюють HTML-форму на основі моделі та перевіряють введені дані."""
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import LoanApplication

# Допустимі межі значень. Модель навчалась на даних у таких діапазонах
# (дохід до ~10000, співзаявник до ~34000, сума займу від 9 до 150 тисяч),
# тому за їх межами прогноз був би ненадійним.
LIMITS = {
    "applicant_income": (1, 20000, "Місячний дохід, від 1 до 20000"),
    "coapplicant_income": (0, 35000, "Від 0 до 35000"),
    "loan_amount": (5, 200, "Сума в ТИСЯЧАХ, від 5 до 200 (наприклад, 120 = 120 тис.)"),
}


class LoanForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            "gender", "married", "dependents", "education", "self_employed",
            "applicant_income", "coapplicant_income", "loan_amount",
            "loan_amount_term", "credit_history", "property_area",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, (low, high, hint) in LIMITS.items():
            field = self.fields[name]
            field.validators.append(MinValueValidator(low))
            field.validators.append(MaxValueValidator(high))
            field.widget.attrs.update({"min": low, "max": high})
            field.help_text = hint
