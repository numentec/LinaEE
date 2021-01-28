from django.db import models


class StakeHolder(models.Manager):

    def get_StakeHolders(self, tipo='all', only_actives=True):

        if 'cli' in tipo:
            if only_actives:
                return self.filter(is_cli=True, is_active=True)
            else:
                return self.filter(is_cli=True)

        if 'prov' in tipo:
            if only_actives:
                return self.filter(is_pro=True, is_active=True)
            else:
                return self.filter(is_pro=True)

        if 'banco' in tipo:
            if only_actives:
                return self.filter(is_soc=True, is_active=True)
            else:
                return self.filter(is_ban=True)

        if 'socio' in tipo:
            if only_actives:
                return self.filter(is_soc=True, is_active=True)
            else:
                return self.filter(is_soc=True)

        if only_actives:
            return self.filter(is_active=True)

        return self.all()

