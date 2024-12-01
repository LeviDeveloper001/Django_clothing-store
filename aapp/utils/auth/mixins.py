from typing import Any
from django.views.generic.base import ContextMixin


class AuthMixin(ContextMixin):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context['user']=user
        context['is_auth'] = user.is_authenticated
        return context

