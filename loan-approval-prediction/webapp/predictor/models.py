"""МОДЕЛІ Django: описують таблицю в базі даних. Кожна заявка (і результат прогнозу) зберігається як один рядок."""
from django.db import models


class LoanApplication(models.Model):
    GENDER = [("Male", "Чоловік"), ("Female", "Жінка")]
    YES_NO = [("Yes", "Так"), ("No", "Ні")]
    DEPENDENTS = [("0", "0"), ("1", "1"), ("2", "2"), ("3+", "3 і більше")]
    EDUCATION = [("Graduate", "Вища освіта"), ("Not Graduate", "Без вищої освіти")]
    TERM = [(12, "12"), (36, "36"), (60, "60"), (84, "84"), (120, "120"),
            (180, "180"), (240, "240"), (300, "300"), (360, "360"), (480, "480")]
    CREDIT = [(1, "Є, хороша"), (0, "Немає або погана")]
    AREA = [("Urban", "Місто"), ("Semiurban", "Передмістя"), ("Rural", "Село")]

    # --- дані, які вводить користувач ---
    gender = models.CharField("Стать", max_length=10, choices=GENDER)
    married = models.CharField("У шлюбі", max_length=3, choices=YES_NO)
    dependents = models.CharField("Кількість утриманців", max_length=2, choices=DEPENDENTS)
    education = models.CharField("Освіта", max_length=15, choices=EDUCATION)
    self_employed = models.CharField("Самозайнятий", max_length=3, choices=YES_NO)
    applicant_income = models.PositiveIntegerField("Дохід заявника")
    coapplicant_income = models.PositiveIntegerField("Дохід співзаявника (0, якщо немає)", default=0)
    loan_amount = models.PositiveIntegerField("Сума займу (у тисячах)")
    loan_amount_term = models.IntegerField("Термін займу (місяців)", choices=TERM, default=360)
    credit_history = models.IntegerField("Кредитна історія", choices=CREDIT)
    property_area = models.CharField("Місцевість", max_length=10, choices=AREA)

    # --- результат роботи моделі ---
    approved = models.BooleanField("Схвалено", default=False)
    probability = models.FloatField("Імовірність схвалення, %", default=0)
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заявка #{self.pk}: {'схвалено' if self.approved else 'відхилено'}"
