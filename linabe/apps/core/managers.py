from django.db import models


class StakeHolder(models.Manager):

    def get_StakeHolders(self, tipo):

        if tipo == 'Cliente':
            return self.filter(is_cli=True)

        if tipo == 'Proveedor':
            return self.filter(is_pro=True)

        if tipo == 'Banco':
            return self.filter(is_ban=True)

        if tipo == 'Socio':
            return self.filter(is_soc=True)

        return self.all()
