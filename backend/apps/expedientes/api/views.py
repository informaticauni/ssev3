from django_filters import rest_framework as filters
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *


class ExpedienteFilter(filters.FilterSet):
    prioridad = filters.CharFilter(field_name='prioridad_id__descripcion', lookup_expr='exact')
    estado = filters.CharFilter(field_name='estado_id__descripcion', lookup_expr='exact')
    descripcion = filters.CharFilter(field_name='descripcion', lookup_expr='icontains')
    tipo_expediente = filters.CharFilter(field_name='tipo_de_expediente_id__descripcion', lookup_expr='icontains')
    fecha_creacion = filters.DateFromToRangeFilter(field_name='fecha_creacion')
    origen = filters.CharFilter(field_name='dependencia_origen_id__descripcion', lookup_expr='icontains')
    destino = filters.CharFilter(field_name='dependencia_destino_id__descripcion', lookup_expr='icontains')

    class Meta:
        model = Expediente
        fields = ('prioridad', 'estado', 'descripcion', 'tipo_expediente', 'fecha_creacion', 'origen', 'destino')


class ExpedienteListView(ListCreateAPIView):
    queryset = Expediente.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ExpedienteFilter

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return ExpedienteNewUpdateSerializer
        return ExpedienteSerializer


@api_view(['GET'])
def expedienteById(request, pk):
    """
    Traer un expediente con su dependencia actual de acuerdo a un ID
    :param request
    :param pk: ID
    :return: Expediente
    """
    try:
        expediente = Expediente.objects.raw(
            'SELECT ee.id, ee.numero_mesa_de_entrada, ee.fecha_actualizacion, ee.dependencia_origen_id, '
            'ee.dependencia_destino_id, ee.descripcion, ei.estado_id, dd.descripcion as dependencia_actual '
            'from expedientes_expediente ee '
            'inner join expedientes_instancia ei on ee.id = ei.expediente_id '
            'inner join dependencias_dependencia dd on ei.dependencia_actual_id = dd.id '
            'where ee.id = %s '
            'order by ei.id desc limit 1 ', [pk]
        )
    except Expediente.DoesNotExist:
        return Response({'Expediente no existe.'}, status=status.HTTP_204_NO_CONTENT)
    expediente_serializer = ExpedienteByIdSerializer(expediente[0])  # sacar el primero
    return Response(expediente_serializer.data)


# sin utilizar por ahora (no se puede editar ni eliminar el expediente)
class ExpedienteDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Expediente.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT']:
            return ExpedienteNewUpdateSerializer
        elif self.request.method in ['PATCH']:
            return ExpedienteNewUpdateSerializer
        return ExpedienteSerializer


# traer todos los expedientes de acuerdo al usuario y a la dependencia en la que esta
class ExpedienteDetail(ListCreateAPIView):
    queryset = Expediente.objects.raw(
        'SELECT expedientes_expediente.id, tipo_de_expediente_id, MAX(expedientes_instancia.id) as instancia_id, '
        'expedientes_instancia.estado_id as estado_instancia, expedientes_expediente.descripcion,'
        'numero_mesa_de_entrada, anho, monto_currency, monto, expedientes_expediente.fecha_creacion, '
        'fecha_actualizacion, dependencia_destino_id, dependencia_origen_id, dependencia_actual_id, lote_id, '
        'objeto_de_gasto_id, prioridad_id '
        'FROM expedientes_expediente '
        'INNER JOIN expedientes_instancia on expedientes_expediente.id = expedientes_instancia.expediente_id '
        'INNER JOIN expedientes_estado on expedientes_estado.id = expedientes_instancia.estado_id '
        'INNER JOIN (SELECT dependencia_id FROM `dependencias_dependencia_por_usuario` as dpu INNER JOIN auth_user on '
        'dpu.usuario_id = auth_user.id WHERE auth_user.id = 1) as dpu on dpu.dependencia_id = '
        'expedientes_instancia.dependencia_actual_id '
        'WHERE expedientes_instancia.estado_id = 1 or expedientes_instancia.estado_id = 2 '
        'GROUP BY expedientes_expediente.id, expedientes_instancia.id')
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ExpedienteFilter

    serializer_class = ExpedienteListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ExpedienteListSerializer(list(queryset), many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return ExpedienteNewUpdateSerializer
        return ExpedienteSerializer


class InstanciaFilter(filters.FilterSet):
    expediente_descripcion = filters.CharFilter(field_name='expediente_id__descripcion', lookup_expr='icontains')
    estado = filters.CharFilter(field_name='estado_id__descripcion', lookup_expr='exact')
    fecha_creacion = filters.DateFromToRangeFilter(field_name='fecha_creacion')
    actual = filters.CharFilter(field_name='dependencia_actual_id__descripcion', lookup_expr='icontains')

    class Meta:
        model = Instancia
        fields = ('expediente_id', 'expediente_descripcion', 'estado', 'fecha_creacion', 'actual')


class InstanciaListView(ListCreateAPIView):
    queryset = Instancia.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = InstanciaFilter

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return InstanciaNewUpdateSerializer
        return InstanciaSerializer


class InstanciaDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Instancia.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT']:
            return InstanciaNewUpdateSerializer
        elif self.request.method in ['PATCH']:
            return InstanciaNewUpdateSerializer
        return InstanciaSerializer


class ComentarioListView(ListCreateAPIView):
    queryset = Comentario.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return ComentarioNewUpdateSerializer
        return ComentarioSerializer


class ComentarioDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT']:
            return ComentarioNewUpdateSerializer
        elif self.request.method in ['PATCH']:
            return ComentarioNewUpdateSerializer
        return ComentarioSerializer


class Objeto_de_GastoListView(ListCreateAPIView):
    queryset = Objeto_de_Gasto.objects.all()
    serializer_class = Objeto_de_GastoSerializer


class Objeto_de_GastoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Objeto_de_Gasto.objects.all()
    serializer_class = Objeto_de_GastoSerializer


class PrioridadListView(ListCreateAPIView):
    queryset = Prioridad.objects.all()
    serializer_class = PrioridadSerializer


class PrioridadDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Prioridad.objects.all()
    serializer_class = PrioridadSerializer


class EstadoListView(ListCreateAPIView):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer


class EstadoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
