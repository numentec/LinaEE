from django.db import models


class StakeHolder(models.Manager):

    def get_StakeHolders(self, tipo):

        if tipo == 'Clientes':
            return self.filter(is_cli=True)

        if tipo == 'Proveedores':
            return self.filter(is_pro=True)

        if tipo == 'Bancos':
            return self.filter(is_ban=True)

        if tipo == 'Socios':
            return self.filter(is_soc=True)
