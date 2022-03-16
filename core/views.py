from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from streamprocessors.kafka_utils import send_kafka_message

import json
import traceback


@csrf_exempt
def send_message_to_kafka(request):
    data = request.POST
    topic = data.get('event_type')
    message = data.get('event_payload')

    response, status = {'status': 'success'}, 200

    try:
        send_kafka_message(topic=topic, message=message)
    except Exception as e:
        response['status'], status = traceback.format_exception_only(type(e), e), 400

    return HttpResponse(json.dumps(response), content_type='application/json', status=status)
