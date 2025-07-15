from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PortfolioItem
from .forms import PortfolioItemForm


@login_required
def portfolio_list(request):
    items = PortfolioItem.objects.filter(user=request.user).select_related('asset')
    return render(request, 'investments/portfolio_list.html', {'items': items})


@login_required
def portfolio_add(request):
    if request.method == 'POST':
        form = PortfolioItemForm(request.POST, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Ativo adicionado à carteira!')
            return redirect('portfolio_list')
    else:
        form = PortfolioItemForm(user=request.user)
    return render(request, 'investments/portfolio_form.html', {'form': form})


@login_required
def portfolio_delete(request, pk):
    item = get_object_or_404(PortfolioItem, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Ativo removido da carteira!')
        return redirect('portfolio_list')
    return render(request, 'investments/portfolio_confirm_delete.html', {'item': item})
