from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction

@login_required
def wallet_dashboard(request):
    wallet = request.user.wallet
    transactions = wallet.transactions.all()
    return render(request, 'wallet/dashboard.html', {'wallet': wallet, 'transactions': transactions})

@login_required
def deposit(request):
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        wallet = request.user.wallet
        wallet.deposit(amount)
        Transaction.objects.create(wallet=wallet, amount=amount, transaction_type="deposit", description="Wallet deposit")
        return redirect('wallet_dashboard')
    return render(request, 'wallet/deposit.html')

@login_required
def withdraw(request):
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        wallet = request.user.wallet
        try:
            wallet.withdraw(amount)
            Transaction.objects.create(wallet=wallet, amount=amount, transaction_type="withdrawal", description="Wallet withdrawal")
            return redirect('wallet_dashboard')
        except ValueError as e:
            return render(request, 'wallet/withdraw.html', {"error": str(e)})
    return render(request, 'wallet/withdraw.html')
