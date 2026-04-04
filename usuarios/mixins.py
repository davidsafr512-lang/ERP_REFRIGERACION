from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'ADMIN'

class SupervisorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol in ['ADMIN', 'SUPER']

class TecnicoRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # El técnico puede ver su parte, pero el admin y super también pueden verla
        return self.request.user.is_authenticated
    