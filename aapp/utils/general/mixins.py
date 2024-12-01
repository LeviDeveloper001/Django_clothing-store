from typing import Any
from utils.auth.mixins import AuthMixin



class GeneralMixin(AuthMixin):
    '''Общий миксин для всех представлений в приложении'''
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # print(context)
        return context


