from django.shortcuts import render, redirect
from medico.models import DadosMedicos, Especialidades, DatasAbertas
from datetime import datetime, timedelta
from .models import Consulta
from django.contrib.messages import add_message, constants

# Create your views here.
def home(request):
    if request.method == "GET":
        medico_filtrar = request.GET.get('medico')
        especialdade_filtrar = request.GET.getlist('especialidades')
        medicos = DadosMedicos.objects.all()
        if medico_filtrar:
            medicos = medicos.filter(nome__icontains=medico_filtrar)
        if especialdade_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialdade_filtrar)
        especialidades = Especialidades.objects.all()
        return render(request, 'home.html', {'medicos': medicos, 'especialidades': especialidades})
    
def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedicos.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user= medico.user).filter(data__gte=datetime.now())
        return render(request, 'escolher_horario.html', {'medico': medico, 'datas_abertas': datas_abertas})

def agendar_horario(request, id_data_aberta):
    if request.method == "GET":

        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente = request.user,
            data_aberta=data_aberta
        )

        horario_agendado.save()

        data_aberta.agendado = True
        data_aberta.save()

        add_message(request, constants.SUCCESS, 'Consulta agendada com sucesso.')

        return redirect('/pacientes/minhas_consultas/')
    
def minhas_consultas(request):
    if request.method == "GET":
        especialidades_filtrar = request.GET.get('especialidades')
        data = request.GET.get('data')
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
        if data:
            data_filtrar = datetime.strptime(data, '%Y-%m-%d')
            minhas_consultas = minhas_consultas.filter(data_aberta__data__gte=data_filtrar-timedelta(days=1))
        return render(request, 'minhas_consultas.html', {'minhas_consultas': minhas_consultas})
