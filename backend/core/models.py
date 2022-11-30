from django.core.validators import MinLengthValidator
from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""

    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class CreatedNameModel(CreatedModel):
    """Абстрактная модель. Добавляет дату создания и поле name."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        validators=[MinLengthValidator(1, 'Пустое поле')]
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
