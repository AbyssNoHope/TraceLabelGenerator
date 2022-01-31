
from LabelGenerator.views import LGView, ResponseData
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST

from backend import services
from backend.models import SpanInformation, TraceInformation
from backend.serializer import SpanSerializer, TraceSerializer


class SpanView(LGView):
    def post(self, request):
        '''
        添加span
        '''
        response_data = ResponseData()
        try:
            trace_uuid = self.check_and_get(
                request.data, 'trace_uuid', response_data)
            services.check_or_create_trace(
                self, request.data, trace_uuid, response_data)
            services.create_span(self, request.data, response_data)
        except ValidationError as e:
            response_data.data = e.detail
            response_data.status = HTTP_400_BAD_REQUEST
        return self.response(response_data)

    def get(self, request, trace_id):
        '''
        获取某一条trace对应的span
        '''
        response_data = ResponseData()
        try:
            spans = SpanInformation.objects.filter(trace=trace_id).order_by(
                'span_start_timestamp')
            response_data.data = SpanSerializer(spans, many=True).data
        except ValidationError as e:
            response_data.data = e.detail
            response_data.status = HTTP_400_BAD_REQUEST
        return self.response(response_data)

    def delete(self, request, trace_id):
        '''
        删除某一条trace对应的span
        '''
        response_data = ResponseData()
        try:
            spans = SpanInformation.objects.filter(trace_id=trace_id)
            spans.delete()
            response_data.data = 'trace%s对应span删除完成' % trace_id
        except ValidationError as e:
            response_data.data = e.detail
            response_data.status = HTTP_400_BAD_REQUEST
        return self.response(response_data)


class TraceView(LGView):
    def post(self, request):
        '''
        修改trace对应的label
        '''
        response_data = ResponseData()
        try:
            trace = services.get_trace(self, request.data, response_data)
            if not trace.checked:
                trace.checked = True
            trace.label = 1-trace.label
            trace.save()
            response_data.data = 'trace状态修改成功，当前trace的label为%s' % trace.label
        except ValidationError as e:
            response_data.data = e.detail
            response_data.status = HTTP_400_BAD_REQUEST
        return self.response(response_data)

    def get(self, request, is_all):
        '''
        获取未打标的trace 或 全部trace
        '''
        response_data = ResponseData()
        try:
            if is_all:
                traces = TraceInformation.objects.all().order_by('trace_start_timestamp')
            else:
                traces = TraceInformation.objects.filter(
                    checked=False).order_by('trace_start_timestamp')
            response_data.data = TraceSerializer(traces, many=True).data
        except ValidationError as e:
            response_data.data = e.detail
            response_data.status = HTTP_400_BAD_REQUEST
        return self.response(response_data)
