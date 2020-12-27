from django.db import models


class StakeHolder(models.Manager):

    def get_StakeHolders(self, tipo):

        if 'cli' in tipo:
            return self.filter(is_cli=True)

        if 'prov' in tipo:
            return self.filter(is_pro=True)

        if 'banco' in tipo:
            return self.filter(is_ban=True)

        if 'socio' in tipo:
            return self.filter(is_soc=True)

        return self.all()
