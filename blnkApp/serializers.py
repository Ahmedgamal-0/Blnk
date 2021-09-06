from rest_framework import serializers
from .models import *

class LoanFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanFund
        fields = ('id','MaxAmount', 'MinAmount', 'InterestRate', 'Duration')
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanFund
        fields = ('id','MaxAmount', 'MinAmount', 'InterestRate', 'Duration')        


class LoanProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProvider
        fields = ('id','Name', 'NationalId', 'MobileNumber')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email')

class LoanTakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanTaker
        fields = ('id','Name', 'NationalId', 'MobileNumber')

class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ('id','Amount', 'Loan', 'status','LoanTaker')

class LoanFundApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanFundApplication
        fields = ('id','Amount', 'LoanFund','status', 'LoanProvider')