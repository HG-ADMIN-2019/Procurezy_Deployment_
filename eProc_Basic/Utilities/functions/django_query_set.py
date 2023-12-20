"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
   django_query_set.py
Usage:


Author:
   Deepika Kodirangaiah
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q, Max

from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Registration.models import UserData


class DjangoQueries:
    @staticmethod
    def django_get_query(model_name, filter_dictionary):
        """
            django get query - use this if you have only one query set result in db table
            model_name: db table class name
            filter_dictionary: values to be filtered
            return: query set result
        """
        try:
            if DjangoQueries().django_existence_check(model_name, filter_dictionary):
                return model_name.objects.get(**filter_dictionary)
            else:
                return None
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def django_existence_check(model_name, filter_dictionary):
        """
            django existence check - use this if you have to check weather filtered value exist in db table or not
            model_name: db table class name
            filter_dictionary: values to be filtered
            return: query set result
        """
        if not filter_dictionary:
            filter_dictionary = {}
        existence_check = model_name.objects.filter(**filter_dictionary).exists()
        return existence_check

    @staticmethod
    def django_queue_existence_check(model_name, filter_dictionary,queue_query):
        """
            django existence check - use this if you have to check weather filtered value exist in db table or not
            model_name: db table class name
            filter_dictionary: values to be filtered
            return: query set result
        """
        if not filter_dictionary:
            filter_dictionary = {}
        existence_check = model_name.objects.filter(queue_query,**filter_dictionary).exists()
        return existence_check

    @staticmethod
    def django_filter_query(model_name, filter_dictionary, ordered_by_list, field_value_lists):
        """
            Django query set which filtered and ordered dictionary list
            model_name: db table class name
            filter_dictionary: values to be filtered
            ordered_by_list: mention for which field need to order(Ascending and descending)
            field_value_lists: list of field required to get result
        """
        if not ordered_by_list:
            ordered_by_list = []
        if not field_value_lists:
            field_value_lists = []
        if not filter_dictionary:
            filter_dictionary = {}
        query_set_result = []
        if DjangoQueries().django_existence_check(model_name, filter_dictionary):
            query_set_result = list(model_name.objects.filter(**filter_dictionary).values(*field_value_lists).order_by(
                *ordered_by_list))
        return query_set_result

    @staticmethod
    def django_filter_query_with_entry_count(model_name, filter_dictionary, ordered_by_list, field_value_lists,entry_count):
        """
            Django query set which filtered and ordered dictionary list
            model_name: db table class name
            filter_dictionary: values to be filtered
            ordered_by_list: mention for which field need to order(Ascending and descending)
            field_value_lists: list of field required to get result
        """
        if not ordered_by_list:
            ordered_by_list = []
        if not field_value_lists:
            field_value_lists = []
        if not filter_dictionary:
            filter_dictionary = {}
        query_set_result = []
        if DjangoQueries().django_existence_check(model_name, filter_dictionary):
            query_set_result = list(model_name.objects.filter(**filter_dictionary).values(*field_value_lists).order_by(
                *ordered_by_list)[:entry_count])
        return query_set_result

    @staticmethod
    def django_queue_query(model_name, filter_dictionary,queue_query, ordered_by_list, field_value_lists):
        """
            Django query set which filtered and ordered dictionary list
            model_name: db table class name
            filter_dictionary: values to be filtered
            ordered_by_list: mention for which field need to order(Ascending and descending)
            field_value_lists: list of field required to get result
        """
        if not ordered_by_list:
            ordered_by_list = []
        if not field_value_lists:
            field_value_lists = []
        if not filter_dictionary:
            filter_dictionary = {}
        query_set_result = []
        if DjangoQueries().django_existence_check(model_name, filter_dictionary):
            query_set_result = list(model_name.objects.filter(queue_query,**filter_dictionary).values(*field_value_lists).order_by(
                *ordered_by_list))
        return query_set_result

    @staticmethod
    def django_queue_query_value_list(model_name, filter_dictionary, queue_query,field_name):
        """
            Django query set which filtered and ordered dictionary list
            model_name: db table class name
            filter_dictionary: values to be filtered
            ordered_by_list: mention for which field need to order(Ascending and descending)
            field_value_lists: list of field required to get result
        """
        if not filter_dictionary:
            filter_dictionary = {}
        field_value_list = []
        if DjangoQueries().django_existence_check(model_name, filter_dictionary):
            field_value_list = list(model_name.objects.filter(queue_query,**filter_dictionary).values_list(field_name, flat=True))
        return field_value_list

    @staticmethod
    def django_filter_value_list_query(model_name, filter_dictionary, field_name):
        """
            Django filter value list query -filter and get mentioned field list
            model_name: db table class name
            filter_dictionary: values to be filtered
            field_name: field name
        """
        field_value_list = list(model_name.objects.filter(**filter_dictionary).values_list(field_name, flat=True).distinct())
        return field_value_list

    @staticmethod
    def django_filter_value_list_without_query(model_name, filter_dictionary, field_name):
        """
            Django filter value list query -filter and get mentioned field list
            model_name: db table class name
            filter_dictionary: values to be filtered
            field_name: field name
        """
        field_value_list = list(
            model_name.objects.filter(**filter_dictionary).values_list(field_name, flat=True))
        return field_value_list

    @staticmethod
    def django_max_filter(model_name, filter_dictionary, field_name):
        max_value = model_name.objects.filter(**filter_dictionary).aggregate(Max(field_name))
        dic_key = field_name+'__max'
        return max_value[dic_key]


    @staticmethod
    def django_filter_count_query(model_name, filter_dictionary):
        """
            django filter count query - gives count for filtered value
            model_name: db table class name
            filter_dictionary: values to be filtered
        """
        return model_name.objects.filter(**filter_dictionary).count()

    @staticmethod
    def django_create_query(model_name, field_value_dictionary):
        """
            Create new entry in database
            model_name: db table class name
            field_value_dictionary: field and its value
        """
        create_entry = model_name.objects.create(**field_value_dictionary)
        return create_entry

    @staticmethod
    def django_bulk_create_query(model_name, field_value_dictionary_list):
        """
            Create new entry in database
            model_name: db table class name
            field_value_dictionary: field and its value
        """
        create_entry = model_name.objects.bulk_create(field_value_dictionary_list)
        return create_entry


    @staticmethod
    def django_update_or_create_query(model_name, filter_dictionary, update_dictionary):
        """
            Create new entry in database
            model_name: db table class name
            filter_dictionary: values to be filtered
        """
        create_entry = model_name.objects.update_or_create(**filter_dictionary, defaults=update_dictionary)
        return create_entry


    @staticmethod
    def django_update_query(model_name, filter_dictionary, update_dictionary):
        """
            Create new entry in database
            model_name: db table class name
            filter_dictionary: values to be filtered
        """
        create_entry = model_name.objects.filter(**filter_dictionary).update(**update_dictionary)
        return create_entry

    @staticmethod
    def django_filter_delete_query(model_name, filter_dictionary):
        """

        """
        return model_name.objects.filter(**filter_dictionary).delete()

    @staticmethod
    def django_filter_only_query(model_name, filter_dictionary):
        return model_name.objects.filter(**filter_dictionary)

    @staticmethod
    def django_filter_value_list_ordered_by_distinct_query(model_name, filter_dictionary, field_name, ordered_by_list):
        """
            Django filter value list query -filter and get mentioned field list
            model_name: db table class name
            filter_dictionary: values to be filtered
            field_name: field name
        """
        if not ordered_by_list:
            ordered_by_list = ''
        field_value_list = list(model_name.objects.filter(**filter_dictionary).values_list(field_name,
                                                                                           flat=True).order_by(
            *ordered_by_list).distinct())
        return field_value_list


def get_user_object_id(username):
    """

    :param username:
    :return:
    """
    object_id = list(UserData.objects.filter(username=username,
                                             client=global_variables.GLOBAL_CLIENT).values_list('object_id',
                                                                                                flat=True))[0]

    return object_id


def bulk_create_entry_db(db_table_name, data_dictionary_list):
    """

    """
    data_dictionary_list_object = [db_table_name(**data_dict) for data_dict in data_dictionary_list]
    create_status = DjangoQueries().django_bulk_create_query(db_table_name, data_dictionary_list_object)
    return create_status


