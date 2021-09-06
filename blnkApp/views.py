from django.shortcuts import render
from .models import *
from rest_framework import  viewsets
from rest_framework.response import  Response
from .serializers import *
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission

class UnauthenticatedPost(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['POST']

class LoanFundViewSet(viewsets.ModelViewSet):
    queryset = LoanFund.objects.all()
    serializer_class = LoanFundSerializer 

class LoanProviderViewSet(viewsets.ModelViewSet):
    queryset = LoanProvider.objects.all()
    serializer_class = LoanProviderSerializer
    permission_classes = [UnauthenticatedPost]

    def create(self, request, *args, **kwargs):
        data=request.data
        user=User.objects.create_user(email=data['email'],password=data['password'])
        user.is_loan_provider=True
        user.save()
        loan_provider=LoanProvider.objects.create(Name=data['Name'],NationalId=data['NationalId'],
        MobileNumber=data['MobileNumber'],user=user)
        loan_provider.save()
        serializer=LoanProviderSerializer(loan_provider)
        return Response(serializer.data)


class LoanTakerViewSet(viewsets.ModelViewSet):
    queryset = LoanTaker.objects.all()
    serializer_class = LoanTakerSerializer
    permission_classes = [UnauthenticatedPost]

    def create(self, request, *args, **kwargs):
        data=request.data
        user=User.objects.create_user(email=data['email'],password=data['password'])
        user.is_loan_Taker=True
        user.save()
        loan_Taker=LoanTaker.objects.create(Name=data['Name'],NationalId=data['NationalId'],
        MobileNumber=data['MobileNumber'],user=user)
        loan_Taker.save()
        serializer=LoanTakerSerializer(loan_Taker)
        return Response(serializer.data)


class BankPersonalViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_bank_clerk=True)
    serializer_class = UserSerializer    
    def create(self, request, *args, **kwargs):
        data=request.data
        flag=data['Flag']
        if flag =='LoanFund':
            loanfund=LoanFund.objects.create(MaxAmount=data['MaxAmount'],MinAmount=data['MinAmount'],InterestRate=data['InterestRate'],Duration=data['Duration'])
            loanfund.save()
            serializer=LoanFundSerializer(loanfund)
            return Response(serializer.data)

        elif flag=='Loan':
            loan=Loan.objects.create(MaxAmount=data['MaxAmount'],MinAmount=data['MinAmount'],InterestRate=data['InterestRate'],Duration=data['Duration'])
            loan.save()
            serializer=LoanSerializer(loan)
            return Response(serializer.data)

def check_fund(amount):
    loan_applications=LoanApplication.objects.all()
    loan_application_amount=0

    for application in loan_applications:
        loan_application_amount+=application.Amount


    loan_fund_applications=LoanFundApplication.objects.all()
    loan_fund_application_amount=0

    for application in loan_fund_applications:
        loan_fund_application_amount+=application.Amount


    net_amount=loan_fund_application_amount-loan_application_amount

    if int(amount)<=net_amount: 
        return True 
    else:
         return False  
    



class LoanApplicationViewSet(viewsets.ModelViewSet):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer    
    def create(self, request, *args, **kwargs):
        data=request.data
        loan_taker = LoanTaker.objects.get(user = request.user)
        loan=Loan.objects.get(id=data['loan_id'])
        if check_fund(data['Amount']):
            loan_application=LoanApplication.objects.create(Amount=data['Amount'],LoanTaker=loan_taker,Loan=loan)
            serializer=LoanApplicationSerializer(loan_application)
            return Response(serializer.data)    

class LoanFundApplicationViewSet(viewsets.ModelViewSet):
    queryset = LoanFundApplication.objects.all()
    serializer_class = LoanFundApplicationSerializer    
    def create(self, request, *args, **kwargs):
        data=request.data
        loan_provider = LoanProvider.objects.get(user = request.user)
        loan_fund=LoanFund.objects.get(id=data['loan_fund_id'])  
        loan_fund_application=LoanFundApplication.objects.create(Amount=data['Amount'],LoanProvider=loan_provider,LoanFund=loan_fund)
        serializer=LoanFundApplicationSerializer(loan_fund_application)
        return Response(serializer.data)


        
        





