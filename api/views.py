from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import ErrorReport
from .serializer import StatusSerializer, ErrorSerializer

# status
@api_view(['GET'])
def get_server_status(request):
    return Response(StatusSerializer({
        'status': 'running', 
        'date': datetime.now()
    }).data)

# Errores
@api_view(['GET'])
def get_errors(request):
    errors = ErrorReport.objects.all() # consulta todos los registros
    return Response(ErrorSerializer(errors, many=True).data) # convierte los objetos a json

@api_view(['GET'])
def get_error_from_code(request, code):
    
    #busca el error
    try: 
        e = ErrorReport.objects.get(code=code)
        
        #devuelve error en json
        return Response(ErrorSerializer(e).data)
    except ErrorReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) # si no existe da error
    
    
# Crear
@api_view(['POST'])
def create_error(request):
    serialized_error = ErrorSerializer(data=request.data) #convierte el json
    if serialized_error.is_valid():
        serialized_error.save() # si es valido lo guarda
        return Response(serialized_error.data, status=status.HTTP_201_CREATED)
    return Response(serialized_error.errors, status=status.HTTP_400_BAD_REQUEST)

# actu o borrar
@api_view(['PUT', 'DELETE'])
def object_update(request, code):
    try:
        obj = ErrorReport.objects.get(code=code) # busca error
        
    except ErrorReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) # si no existe error

    if request.method == 'PUT':
        serialized_data = ErrorSerializer(obj, data=request.data)
        #valida, guarda y devuelve lo actualizado
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST) # error

    if request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)