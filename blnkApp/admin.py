from django.contrib import admin
from .models import *

admin.site.register(LoanProvider)
admin.site.register(LoanTaker)
admin.site.register(LoanFund)
admin.site.register(Loan)
admin.site.register(LoanFundApplication)
admin.site.register(LoanApplication)
admin.site.register(User)
