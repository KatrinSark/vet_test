from django.db import models


class Client(models.Model):
    """Клиент."""
    name = models.CharField(verbose_name="Имя", max_length=150)
    surname = models.CharField(verbose_name="Фамилия", max_length=150)
    phone = models.CharField(verbose_name="Телефон", max_length=15)
    telegram_id = models.CharField(max_length=300, unique=True, primary_key=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self) -> str:
        return f"{self.pk} -- {self.name} {self.surname}"


class Appointment(models.Model):
    """
    Запись на прием
    """
    date = models.DateTimeField(verbose_name="Дата записи")
    pet = models.CharField(verbose_name="Вид животного", max_length=200)
    owner = models.ForeignKey(
        verbose_name="Хозяин", to=Client, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"

    def __str__(self) -> str:
        return f"#{self.pk} {self.pet}"
