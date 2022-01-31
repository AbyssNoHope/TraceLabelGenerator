from rest_framework.exceptions import ValidationError

from backend.views import LGView, ResponseData

from .models import TraceInformation
from .serializer import SpanSerializer, TraceSerializer


def check_or_create_trace(self: LGView, request_data, trace_uuid, response_data: ResponseData):
    try:
        TraceInformation.objects.get(trace_uuid=trace_uuid)
    except TraceInformation.DoesNotExist:
        try:
            trace_start_timestamp = self.check_and_get(
                request_data, 'trace_start_timestamp', response_data)
            label = self.check_and_get(
                request_data, 'label', response_data)
            if label == 'False':
                label = False
            elif label == 'True':
                label = True
        except ValidationError as err:
            raise ValidationError(err.detail)

        trace_serializer = TraceSerializer(data={
            'trace_uuid': trace_uuid,
            'trace_start_timestamp': trace_start_timestamp,
            'label': label,
            'checked': False
        })
        if trace_serializer.is_valid():
            trace_serializer.save()
        else:
            raise ValidationError('新建trace失败' + trace_serializer.errors)


def create_span(self: LGView, request_data, response_data: ResponseData):
    try:
        trace_uuid = self.check_and_get(
            request_data, 'trace_uuid', response_data)
        trace = TraceInformation.objects.get(trace_uuid=trace_uuid)
        span_uuid = self.check_and_get(
            request_data, 'span_uuid', response_data)
        parent_span_uuid = self.check_and_get(
            request_data, 'parent_span_uuid', response_data)
        span_start_timestamp = self.check_and_get(
            request_data, 'span_start_timestamp', response_data)
        duration = self.check_and_get(
            request_data, 'duration', response_data)
        operation_name = self.check_and_get(
            request_data, 'operation_name', response_data)
        service_name = self.check_and_get(
            request_data, 'service_name', response_data)
        error_message = self.check_and_get(
            request_data, 'error_message', response_data)
        span_serializer = SpanSerializer(data={
            'trace': trace.id,
            'span_uuid': span_uuid,
            'parent_span_uuid': parent_span_uuid,
            'span_start_timestamp': span_start_timestamp,
            'duration': duration,
            'operation_name': operation_name,
            'service_name': service_name,
            'error_message': error_message
        })
        if not span_serializer.is_valid():
            raise ValidationError('新建span失败'+str(span_serializer.errors))
        span = span_serializer.save()
        response_data.data = SpanSerializer(span).data
    except ValidationError as err:
        raise ValidationError(err)


def get_trace(self: LGView, request_data, response_data: ResponseData):
    try:
        trace_id = self.check_and_get(
            request_data, 'trace_id', response_data)
        trace = TraceInformation.objects.get(id=trace_id)
        return trace
    except TraceInformation.DoesNotExist:
        raise ValidationError('所请求的trace不存在')
