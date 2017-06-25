# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail


def validate_cad_file(file):
    LIMIT = 25 * 1024 * 1024  # 25MB
    valid_extensions = ['.stl', '.dxf']
    import os
    ext = os.path.splitext(file.name)[1]
    if ext not in valid_extensions:
        raise ValidationError(
            "Tipo de arquivo não suportado, somente arquivos DXF ou STL")
    if file.size > LIMIT:
        raise ValidationError("Arquivo muito grande, tamanho máximo de 25 MB")


def validate_gcode_file(file):
    LIMIT = 25 * 1024 * 1024  # 25MB
    valid_extensions = ['.gcode', '.ngc']
    import os
    ext = os.path.splitext(file.name)[1]
    if ext not in valid_extensions:
        raise ValidationError(
            "Tipo de arquivo não suportado, somente arquivos gcode e ngc")
    if file.size > LIMIT:
        raise ValidationError("Arquivo muito grande, tamanho máximo de 25 MB")


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'cad_files/{0}/{1}'.format(instance.owner.username, filename)


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
    LASER = 0
    MILLING = 1
    CNC_OPT = (
        (LASER, "Marcação a laser"),
        (MILLING, "Corte com fresa")
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
        "Arquivo CAD",
        upload_to=user_directory_path,
        validators=[validate_cad_file])
    g_code = models.FileField(
        "Arquivo G-code",
        upload_to=user_directory_path,
        validators=[validate_gcode_file], blank=True)
    cnc_option = models.IntegerField(
        "Tipo de solicitação", choices=CNC_OPT, default=MILLING)

    def __str__(self):
        return (str(self.sent_at) + " | " + str(self.owner) +
                " (" + self.get_status_display() +
                ") - aprovado por: " + str(self.approved_by))

    def is_available_for_cancelling(self):
        available = True
        if self.status not in [Request.RECEIVED, Request.APPROVED]:
            available = False
        return available

    def approve(self):
        if not self.status == Request.RECEIVED:
            # Resquest is approvable for status = Received
            raise ValidationError
        req.status = IN_PROGRESS
        success = False
        try:
            subject = str(self.pk)
            with open(self.g_code, 'r') as g_code:
                message = g_code.read().replace('\n', '')
            from_email = 'pereirasallan@gmail.com'
            recipient = ['pereirasallan@gmail.com']
            send_mail(subject, message, from_email,
                      recipient, fail_silently=False)
            success = True
        except Exception as e:
            print(e)
        return success

    def delete(self, *args, **kwargs):
        try:
            self.cad_file.delete()
        except:
            pass
        super(Request, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"
