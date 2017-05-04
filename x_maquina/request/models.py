from django.db import models
from django.contrib.auth.models import User


class Request(models.Model):
    RECEIVED = 0
    IN_PROGRESS = 1
    APPROVED = 2
    CANCELLED = 3
    SUCCESS = 4
    FAILED = 5
    STATUS = (
        (RECEIVED, 'Recebido'),
        (APPROVED, 'Aprovado'),
        (IN_PROGRESS, 'Em Andamento'),
        (CANCELLED, 'Cancelado'),
        (SUCCESS, 'Finalizado com Sucesso'),
        (FAILED, 'Finalizado com Falha'),
    )
    status = models.IntegerField("Status", choices=STATUS, default=RECEIVED)
    sent_at = models.DateField("Enviado em")
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
    cad_file = models.FileField("Arquivo STL")

    def __str__(self):
        return str(self.sent_at) + " | " + self.owner + \
            " - aprovado por: " + self.approved_by

    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"
