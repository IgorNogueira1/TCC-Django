import io, xlsxwriter, json
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth import logout
from reportlab.pdfgen import canvas
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transacao, Categoria
from .forms import (
    UserRegistrationForm,
    TransacaoForm,
    CategoriaForm,
    UserUpdateForm,
)
from django.utils.timezone import now
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import calendar

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})





def logout_view(request):
    logout(request)
    return redirect('index')  # ou a URL que quiser redirecionar


@login_required
def profile_detail(request):
    return render(request, 'core/profile_detail.html', {'user_obj': request.user, 'title': 'Perfil'})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('dashboard')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'core/profile_form.html', {'form': form, 'title': 'Editar Perfil'})



@login_required
def dashboard(request):
    hoje = timezone.now()

    # Coleta mês e ano do GET ou usa os atuais
    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))

    # Calcula o intervalo de datas do mês selecionado
    primeiro_dia_mes = datetime(ano, mes, 1)
    ultimo_dia_mes = (primeiro_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Transações filtradas por usuário e intervalo de data
    transacoes_mes = Transacao.objects.filter(
        usuario=request.user,
        data__gte=primeiro_dia_mes,
        data__lte=ultimo_dia_mes
    )

    # Cálculos financeiros
    total_receitas = transacoes_mes.filter(tipo='receita').aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = transacoes_mes.filter(tipo='despesa').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = total_receitas - total_despesas

    # Transações recentes (limitadas às do mês filtrado)
    ultimas_transacoes = transacoes_mes.order_by('-data')[:5]

    # Gráficos - despesas por categoria
    categorias_despesas_agg = transacoes_mes.filter(tipo='despesa').values('categoria__nome').annotate(total=Sum('valor'))
    categorias_despesas = [item['categoria__nome'] for item in categorias_despesas_agg]
    valores_despesas = [float(item['total']) for item in categorias_despesas_agg]

    # Gráficos - receitas por categoria
    categorias_receitas_agg = transacoes_mes.filter(tipo='receita').values('categoria__nome').annotate(total=Sum('valor'))
    categorias_receitas = [item['categoria__nome'] for item in categorias_receitas_agg]
    valores_receitas = [float(item['total']) for item in categorias_receitas_agg]

    # Dados para filtros
    meses = [(i, calendar.month_name[i]) for i in range(1, 13)]
    anos = list(range(2022, hoje.year + 1))

    # Contexto para o template
    context = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'ultimas_transacoes': ultimas_transacoes,
        'categorias_despesas_json': json.dumps(categorias_despesas),
        'valores_despesas_json': json.dumps(valores_despesas),
        'categorias_receitas_json': json.dumps(categorias_receitas),
        'valores_receitas_json': json.dumps(valores_receitas),
        'mes_atual': mes,
        'ano_atual': ano,
        'meses': meses,
        'anos': anos,
        'hoje': hoje,
    }

    return render(request, 'core/dashboard.html', context)




@login_required
def transacao_list(request):
    hoje = timezone.now()

    # Pega mês e ano do GET, ou usa o atual
    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))

    # Calcula intervalo de datas do mês
    primeiro_dia = datetime(ano, mes, 1)
    ultimo_dia = (primeiro_dia.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

    # Filtra transações por usuário e período
    transacoes = Transacao.objects.filter(
        usuario=request.user,
        data__range=(primeiro_dia, ultimo_dia)
    ).order_by('-data')

    # Lista de meses e anos para o filtro
    meses = [(i, calendar.month_name[i]) for i in range(1, 13)]
    anos = list(range(2022, hoje.year + 1))

    return render(request, 'core/transacao_list.html', {
        'transacoes': transacoes,
        'mes_atual': mes,
        'ano_atual': ano,
        'meses': meses,
        'anos': anos,
    })


@login_required
def transacao_create(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST, user=request.user)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.usuario = request.user
            transacao.save()
            messages.success(request, 'Transação criada com sucesso!')
            return redirect('transacao_list')
    else:
        form = TransacaoForm(user=request.user)

    categorias = Categoria.objects.filter(usuario=request.user)

    return render(request, 'core/transacao_form.html', {
        'form': form,
        'categorias': categorias,  # <-- necessário para popular o <select>
        'title': 'Nova Transação'
    })

@login_required
def transacao_edit(request, pk):
    transacao = get_object_or_404(Transacao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = TransacaoForm(request.POST, instance=transacao, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transação atualizada com sucesso!')
            return redirect('transacao_list')
    else:
        form = TransacaoForm(instance=transacao, user=request.user)

    categorias = Categoria.objects.filter(usuario=request.user)  # <- Adicione isso

    return render(request, 'core/transacao_form.html', {
        'form': form,
        'categorias': categorias,  # <- Envie para o template
        'title': 'Editar Transação'
    })


@login_required
def transacao_delete(request, pk):
    transacao = get_object_or_404(Transacao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        transacao.delete()
        messages.success(request, 'Transação excluída com sucesso!')
        return redirect('transacao_list')
    return render(request, 'core/transacao_confirm_delete.html', {'transacao': transacao})

@login_required
def categoria_list(request):
    categorias = Categoria.objects.filter(usuario=request.user)
    return render(request, 'core/categoria_list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'core/categoria_form.html', {'form': form, 'title': 'Nova Categoria'})

@login_required
def categoria_edit(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'core/categoria_form.html', {'form': form, 'title': 'Editar Categoria'})

@login_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, usuario=request.user)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('categoria_list')
    return render(request, 'core/categoria_confirm_delete.html', {'categoria': categoria})



#teste para exportar escolhendo os meses
@login_required
def exportar_excel(request):
    mes = int(request.GET.get('mes', timezone.now().month))
    ano = int(request.GET.get('ano', timezone.now().year))
    primeiro_dia = datetime(ano, mes, 1)
    ultimo_dia = (primeiro_dia + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    receitas = Transacao.objects.filter(usuario=request.user, tipo='receita', data__range=[primeiro_dia, ultimo_dia])
    despesas = Transacao.objects.filter(usuario=request.user, tipo='despesa', data__range=[primeiro_dia, ultimo_dia])

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    bold = workbook.add_format({'bold': True, 'bg_color': '#DCE6F1'})
    money = workbook.add_format({'num_format': 'R$ #,##0.00'})

    # Aba Receitas
    receita_sheet = workbook.add_worksheet("Receitas")
    receita_sheet.write_row(0, 0, ['Data', 'Categoria', 'Valor'], bold)
    total_receita = 0
    for i, t in enumerate(receitas, start=1):
        receita_sheet.write(i, 0, t.data.strftime('%d/%m/%Y'))
        receita_sheet.write(i, 1, t.categoria.nome)
        receita_sheet.write(i, 2, t.valor, money)
        total_receita += t.valor
    receita_sheet.write(len(receitas) + 2, 1, 'Total:', bold)
    receita_sheet.write(len(receitas) + 2, 2, total_receita, money)

    # Aba Despesas
    despesa_sheet = workbook.add_worksheet("Despesas")
    despesa_sheet.write_row(0, 0, ['Data', 'Categoria', 'Valor'], bold)
    total_despesa = 0
    for i, t in enumerate(despesas, start=1):
        despesa_sheet.write(i, 0, t.data.strftime('%d/%m/%Y'))
        despesa_sheet.write(i, 1, t.categoria.nome)
        despesa_sheet.write(i, 2, t.valor, money)
        total_despesa += t.valor
    despesa_sheet.write(len(despesas) + 2, 1, 'Total:', bold)
    despesa_sheet.write(len(despesas) + 2, 2, total_despesa, money)

    # Aba Resumo
    resumo_sheet = workbook.add_worksheet("Resumo")
    resumo_sheet.write_column(0, 0, ['Total Receitas', 'Total Despesas', 'Saldo'], bold)
    resumo_sheet.write_column(0, 1, [total_receita, total_despesa, total_receita - total_despesa], money)

    workbook.close()
    output.seek(0)
    return HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={
        'Content-Disposition': f'attachment; filename="relatorio_{mes:02d}_{ano}.xlsx"'
    })


@login_required
def exportar_pdf(request):
    mes = int(request.GET.get('mes', timezone.now().month))
    ano = int(request.GET.get('ano', timezone.now().year))
    primeiro_dia = datetime(ano, mes, 1)
    ultimo_dia = (primeiro_dia + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    receitas = Transacao.objects.filter(usuario=request.user, tipo='receita', data__range=[primeiro_dia, ultimo_dia])
    despesas = Transacao.objects.filter(usuario=request.user, tipo='despesa', data__range=[primeiro_dia, ultimo_dia])

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Relatório Financeiro - {mes:02d}/{ano}", styles['Title']))
    elements.append(Spacer(1, 12))

    def gerar_tabela(titulo, transacoes):
        data = [["Data", "Categoria", "Valor"]] + [
            [t.data.strftime('%d/%m/%Y'), t.categoria.nome, f"R$ {t.valor:.2f}"] for t in transacoes
        ]
        total = sum(t.valor for t in transacoes)
        data.append(["", "Total", f"R$ {total:.2f}"])

        table = Table(data, colWidths=[80, 250, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DCE6F1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#000000')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ]))
        elements.append(Paragraph(titulo, styles['Heading2']))
        elements.append(table)
        elements.append(Spacer(1, 24))

    gerar_tabela("Receitas", receitas)
    gerar_tabela("Despesas", despesas)

    saldo = sum(t.valor for t in receitas) - sum(t.valor for t in despesas)
    elements.append(Paragraph(f"<b>Saldo do Mês:</b> R$ {saldo:.2f}", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf', headers={
        'Content-Disposition': f'attachment; filename="relatorio_{mes:02d}_{ano}.pdf"'
    }) 