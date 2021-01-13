# from django.contrib.postgres.fields import JSONField
from enum import Enum

from django.db import models
from django.db.models import JSONField
from django.utils.translation import ugettext_lazy

from core.cache import BaseCache


class CoreEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: [c.name, c.value], cls))

    @classmethod
    def choose_list(cls):
        return list(map(lambda c: [c.value, ' '.join(
            x.capitalize() or '_' for x in c.value.split('_'))], cls))


class CoreModel(models.Model, BaseCache):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=ugettext_lazy('Created At'))
    created_by = models.ForeignKey(
        "auth.User", on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="%(app_label)s_%(class)s_created_by",
        verbose_name=ugettext_lazy('Created By')
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=True,
        blank=True, verbose_name=ugettext_lazy('Updated At'))
    updated_by = models.ForeignKey(
        "auth.User", on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="%(app_label)s_%(class)s_updated_by",
        verbose_name=ugettext_lazy('Updated By')
    )
    is_active = models.BooleanField(default=True, verbose_name=ugettext_lazy('Is Active'))
    is_deleted = models.BooleanField(
        default=False, verbose_name=ugettext_lazy('Is Deleted'))
    deleted_at = models.DateTimeField(
        null=True, blank=True, verbose_name=ugettext_lazy('Deleted At'))
    deleted_by = models.ForeignKey(
        "auth.User", on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="%(app_label)s_%(class)s_deleted_by",
        verbose_name=ugettext_lazy('Deleted By')
    )
    data = JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True
        ordering = ["id"]

    def save(self, user=None, *args, **kwargs):
        if not self.id:
            if user:
                self.created_by = user
        else:
            if user:
                self.updated_by = user

        super().save(*args, **kwargs)

        self.del_cache(self.id)