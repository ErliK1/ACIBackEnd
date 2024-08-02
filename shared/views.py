import abc
import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework import serializers, status
from rest_framework.response import Response

from shared.constants import DATA, ERRORS, SERIALIZER_ERROR_MESSAGE

from shared.utils import get_error_message


# Create your views here.



class ACIListAPIView(ListAPIView, abc.ABC):
    filter_serializer_class = None
    filter_map = {}
    order_params = None

    # ToDo - Add Paginator

    # ToDo - Perpiqu ta pergatisesh per list serializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.order_queryset(queryset)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def filter_queryset(self, queryset):
        query_params_for_filter = self.request.query_params.get('filter')
        exact = False
        if not query_params_for_filter:
            query_params_for_filter = self.request.query_params.get('exact')
            exact = True
        if query_params_for_filter:
            serializer = self.get_serializer(json.loads(query_params_for_filter))
            return queryset.filter(self.find_filter_kwargs(serializer, exact))
        return queryset

    def find_filter_kwargs(self, serializer: serializers.Serializer, exact):
        dictionary_filter_kwargs = {self.find_lookup_key(serializer, k, exact): v for k, v in serializer.validated_data
                                    if v or v is not False}
        return Q(**dictionary_filter_kwargs)

    def find_lookup_key(self, serializer: serializers.Serializer, key, exact):
        if not exact and isinstance(serializer.fields.get(key), serializers.CharField):
            return '{}__icontains'.format(self.filter_map.get(key))
        return self.filter_map.get(key)

    def get_filter_serializer_class(self):
        return self.filter_serializer_class

    def get_filter_serializer(self, data):
        try:
            serializer = self.get_serializer_class()(data=data)
            serializer.is_valid(raise_exception=True)
            return serializer
        except Exception as e:
            raise ValidationError(str(e))

    def order_queryset(self, query_set):
        sort_by = self.request.query_params.get('sort')
        order_by = self.request.query_params.get('order')
        if sort_by and order_by:
            if order_by == 'asc':
                return query_set.order_by(*[self.filter_map.get(element) for element in sort_by])
            else:
                return query_set.order_by(
                    *list(map(lambda x: '-' + str(x), [self.filter_map.get(element) for element in sort_by])))
        return query_set


class ACICreateAPIView(CreateAPIView, abc.ABC):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        response_data = {}
        respones_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_headers = None
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            header = self.get_success_headers(serializer.data)
            response_data = {DATA: serializer.data}
            response_stauts = status.HTTP_201_CREATED
            response_headers = header
        except ValidationError as ve:
            response_data = {ERRORS: ve.get_full_details()}
            response_stauts = status.HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist as odne:
            response_data = {ERRORS: 'Object does not exists: {}'.format(str(odne))}
        except IntegrityError as ie:
            response_data = {ERRORS: 'Duplicated values'}
        except Exception as e:
            response_data = {ERRORS: str(e)}
        finally:
            return Response(response_data, status=respones_status, headers=response_headers)


class ACIListCreateAPIView(ACICreateAPIView, ACIListAPIView):
    read_serializer_class = None
    write_serializer_class = None
    serializer_error_message = SERIALIZER_ERROR_MESSAGE

    def get_serializer_class(self):
        if self.request.method == 'GET':
            assert self.read_serializer_class or self.serializer_class, get_error_message(self.serializer_error_message, self.__class__.__name__)
            return self.read_serializer_class if self.read_serializer_class else self.serializer_class
        if self.request.method == 'POST':
            assert self.write_serializer_class or self.serializer_class, get_error_message(self.serializer_error_message, self.__class__.__name__)
            return self.write_serializer_class if self.write_serializer_class else self.serializer_class
        assert self.serializer_class, get_error_message(self.serializer_error_message, self.__class__.__name__)
        return self.serializer_class


class ACIRetrieveAPIView(RetrieveAPIView, abc.ABC):
    serializer_class = None
    read_serializer_class = None
    serializer_error_message = SERIALIZER_ERROR_MESSAGE

    def get_serializer_class(self):
        assert self.serializer_class or self.read_serializer_class, get_error_message(self.serializer_error_message, self.__class__.__name__)
        return self.serializer_class if self.serializer_class else self.read_serializer_class








