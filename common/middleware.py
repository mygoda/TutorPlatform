# coding=utf-8
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import logging

from requests import Response
from rest_framework import renderers
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger.renderers import OpenAPIRenderer

from .exception import ServerException
from libs.http import error_json_response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import BaseRenderer, JSONRenderer, CoreJSONRenderer
import traceback
from . import exception
from . import models
from customer import models as customer_models

logger = logging.getLogger(__name__)

SKIP_URLS = [
    "/admin",
]


class CommonMiddleware(MiddlewareMixin):
    """基础中间层"""

    def process_request(self, request):
        if request.META.get("HTTP_CITYID"):
            request.city = models.City.objects.get(id=request.META.get("HTTP_CITYID"))

        if request.META.get("HTTP_TOKEN"):
            request.customer = customer_models.CustomerTokenShip.get_customer_by_token(request.META.get("HTTP_TOKEN"))
        else:
            request.customer = None


class ProcessExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        """
            处理异常
        :param request:
        :param exception:
        :return:
        """
        logger.info("error %s" % traceback.format_exc())
        if isinstance(exception, ServerException):
            return error_json_response({"message": str(exception)})


class ProcessCORSMiddleware(MiddlewareMixin):

    def add_cors_header(self, origin, response):
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        response[
            'Access-Control-Allow-Headers'
        ] = 'reqid, nid, host, x-real-ip, x-forwarded-ip, event-type, event-id, accept, content-type, accept-encoding, country'

    def process_request(self, request):

        request._dont_enforce_csrf_checks = True  # For csrf
        if request.method == 'OPTIONS':
            response = HttpResponse(status=204)
            self.add_cors_header(request.META.get('HTTP_ORIGIN'), response)
            return response

    def process_response(self, request, response):

        if request.META.get('HTTP_ACCEPT') == 'application/json':
            self.add_cors_header(request.META.get('HTTP_ORIGIN'), response)
        return response


