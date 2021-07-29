from django.db import models
from django.utils import timezone


class AbstractModel(models.Model):
    created_time = models.DateTimeField(
        default=timezone.now,
    )

    @classmethod
    def create(cls, **kwargs):
        try:
            obj = cls(
                **kwargs
            )
            obj.save()
            return obj
        except Exception as e:
            print(e.args, " error on create")
            return None

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs)

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            return cls.objects.get(*args, **kwargs)
        except Exception as e:
            # print(e.args, " error on get")
            return cls.objects.filter(*args, **kwargs).first()

    @classmethod
    def all(cls):
        return cls.objects.all()

    def get_created_time(self):
        return self.created_time.strftime("%d.%m.%Y %H:%M:%S")

    class Meta:
        abstract = True
