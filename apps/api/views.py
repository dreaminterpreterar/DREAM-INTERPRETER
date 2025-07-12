from .models import Parameter, Interpretation
from .serializers import InterpretationCreateSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from openai import OpenAI

class GetInterpretationsView(APIView):
    def get(self, request, user, *args, **kwargs):
        interpretations = Interpretation.objects.filter(user=user)

        if not interpretations.exists():
            return Response({
                'type': 'error',
                'title': 'Error de datos',
                'message': 'No se encontraron interpretaciones para este usuario.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = InterpretationCreateSerializer(interpretations, many=True)
        return Response({
            'type': 'success',
            'title': 'Operación exitosa',
            'message': 'Interpretaciones encontradas.',
            'interpretations': serializer.data
        }, status=status.HTTP_200_OK)

class CreateInterpretationView(APIView):
    def post(self, request, *args, **kwargs):
        interpretation_serializer = InterpretationCreateSerializer(data=request.data)

        if not interpretation_serializer.is_valid():
            fields_errors = interpretation_serializer.errors.keys()

            if 'dream' in fields_errors:
                return Response({
                    'type': 'error',
                    'title': 'Error de campos',
                    'message': 'Por favor ingrese un sueño para poder interpretarlo.'
                }, status=status.HTTP_400_BAD_REQUEST)

            if 'user' in fields_errors:
                return Response({
                    'type': 'error',
                    'title': 'Error de validacion',
                    'message': 'El campo id es requerido, espere a que se recargue la pagina y vuelva a intentarlo.',
                    'action': 'reload'
                }, status=status.HTTP_400_BAD_REQUEST)

        missing_parameters = []

        system_prompt = Parameter.objects.filter(name='system_prompt').first()
        if system_prompt is None:
            missing_parameters.append('system_prompt')

        ai_model = Parameter.objects.filter(name='ai_model').first()
        if ai_model is None:
            missing_parameters.append('ai_model')

        base_url = Parameter.objects.filter(name='base_url').first()
        if base_url is None:
            missing_parameters.append('base_url')

        api_key = Parameter.objects.filter(name='api_key').first()
        if api_key is None:
            missing_parameters.append('api_key')

        if not system_prompt or not api_key or not base_url:
            return Response({
                'type': 'error',
                'title': 'Error de parametros', 
                'message': f"Asegurese de que los siguientes parametros esten configurados: {', '.join([f"'{param}'" for param in missing_parameters])}."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        system_prompt_value = system_prompt.value
        ai_model_value = ai_model.value
        base_url_value = base_url.value
        api_key_value = api_key.value

        try:
            client = OpenAI(
                base_url=base_url_value,
                api_key=api_key_value,
            )

            completion = client.chat.completions.create(
                model=ai_model_value,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt_value
                    },
                    {
                        "role": "user",
                        "content": request.data['dream']
                    }
                ]
            )

            interpretation_text = completion.choices[0].message.content

            interpretation_serializer.save(interpretation=interpretation_text)

            return Response({
                'type': 'success',
                'title': 'Operacion exitosa',
                'message': 'Sueño interpretado correctamente.',
                'interpretation': interpretation_text
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)

            return Response({
                'type': 'error',
                'title': 'Error de OpenAI.',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)