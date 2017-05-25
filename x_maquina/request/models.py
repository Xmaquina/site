# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_stl_file(file):
    LIMIT = 25 * 1024 * 1024  # 25MB
    valid_extensions = ['.stl']
    import os
    ext = os.path.splitext(file.name)[1]
    if ext not in valid_extensions:
        raise ValidationError(
            "Tipo de arquivo não suportado, somente arquivos STL")
    if file.size > LIMIT:
        raise ValidationError("Arquivo muito grande, tamanho máximo de 25 MB")


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'cad_files/user_{0}/{1}'.format(instance.owner.id, filename)


class Request(models.Model):
    RECEIVED = 0
    IN_PROGRESS = 1
    APPROVED = 2
    CANCELLED = 3
    SUCCESS = 4
    FAILED = 5
    STATUS = (
        (RECEIVED, 'Aguardando aprovação'),
        (APPROVED, 'Aprovado'),
        (IN_PROGRESS, 'Em andamento'),
        (CANCELLED, 'Cancelado'),
        (SUCCESS, 'Finalizado com sucesso'),
        (FAILED, 'Finalizado com falha'),
    )
    status = models.IntegerField("Status", choices=STATUS, default=RECEIVED)
    sent_at = models.DateTimeField("Enviado em", auto_now=True)
    owner = models.ForeignKey(
        User,
        verbose_name="Proprietário",
        related_name="owner",
        on_delete=models.CASCADE)
    approved_by = models.ForeignKey(
        User,
        verbose_name="Aprovado por",
        related_name="approved_by",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to={
            'is_staff': True})
    cad_file = models.FileField(
        "Arquivo STL",
        upload_to=user_directory_path,
        validators=[validate_stl_file])

    def __str__(self):
        return str(self.sent_at) + " | " + str(self.owner) + \
            " - aprovado por: " + str(self.approved_by)

    def delete(self, *args, **kwargs):
        try:
            self.cad_file.delete()
        except:
            pass
        super(Request, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"
