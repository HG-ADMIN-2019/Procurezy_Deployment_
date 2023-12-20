"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
   attributes_generic.py
Usage:


Author:
   Deepika Kodirangaiah
"""
from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.sort_dictionary import sort_list_dictionary_key_values
from eProc_Basic.Utilities.global_defination import global_variables


class OrgAttributeValues:

    @staticmethod
    def get_org_attr_values_list(acc_drop_down_list, object_id_list, exclude_acc_list, acc_list):
        """

        :param acc_list:
        :param object_id_list:
        :return:
        """
        unique_drop_down_list = list(set(acc_drop_down_list))
        actual_exclude = []

        # get actual exclude and ignore exclude list
        ignore_exclude_list, exclude_list = OrgAttributeValues.get_ignore_exclude_list(exclude_acc_list, acc_list,
                                                                                       object_id_list)

        # remove  exclude value from ignore list
        for exclude_value in exclude_list:
            if exclude_value not in ignore_exclude_list:
                actual_exclude.append(exclude_value)
                unique_drop_down_list.remove(exclude_value)

        return unique_drop_down_list, actual_exclude

    @staticmethod
    def get_org_attr_default_value(attr_value_list, exclude_list):
        """

        :param attr_value_list:
        :param exclude_list:
        :return:
        """
        exclude_attr_list = []
        default_attr = ''
        for attr_value in attr_value_list:
            if attr_value['attr_level_exclude']:
                exclude_attr_list.append(attr_value["low"])
            if attr_value['attr_level_default']:
                if attr_value["low"] not in exclude_attr_list:
                    default_attr = attr_value["low"]
                    break
        if default_attr in exclude_list:
            default_attr.clear()
        return default_attr

    @staticmethod
    def get_ignore_exclude_list(exclude_acc_list, acc_list, object_id_list):
        """

        :param exclude_acc_list:
        :param acc_list:
        :return:
        """
        ignore_exclude_list = []
        exclude_list = []
        for exclude_count, exclude_acc in enumerate(exclude_acc_list):
            exclude_list.append(exclude_acc['low'])
            for acc_lists in acc_list:
                if acc_lists['low'] == exclude_acc['low']:
                    if not acc_lists['attr_level_exclude']:
                        acc_index = object_id_list.index(acc_lists['object_id'])
                        exclude_index = object_id_list.index(exclude_acc['object_id'])
                        if acc_index < exclude_index:
                            ignore_exclude_list.append(exclude_acc['low'])
        return ignore_exclude_list, exclude_list

    @staticmethod
    def get_configured_attr_values_attr_default(attr_low_value_list, object_id_list, exclude_detail_list,
                                                attr_id_attr_level_detail_list):
        """

        :param attr_low_value_list:
        :param object_id_list:
        :param exclude_detail_list:
        :param attr_id_attr_level_detail_list:
        :return:
        """
        error_msg = ''
        attr_low_value_list, exclude_list = OrgAttributeValues.get_org_attr_values_list(attr_low_value_list,
                                                                                        object_id_list,
                                                                                        exclude_detail_list,
                                                                                        attr_id_attr_level_detail_list)
        default_acc_list = OrgAttributeValues.get_org_attr_default_value(attr_id_attr_level_detail_list, exclude_list)
        if default_acc_list:
            attr_low_value_list.remove(default_acc_list)
            attr_low_value_list.insert(0, default_acc_list)

        return attr_low_value_list, default_acc_list

    @staticmethod
    def get_attr_value_and_exclude_detail(attr_detail_list):
        exclude_details = []
        attr_value_list = []
        for attr_detail in attr_detail_list:
            exclude_dic = {}
            if attr_detail['attr_level_exclude']:
                exclude_dic['low'] = attr_detail['low']
                exclude_dic['object_id'] = attr_detail['object_id']
                exclude_details.append(exclude_dic)
            attr_value_list.append(attr_detail['low'])

        return attr_value_list, exclude_details

    @staticmethod
    def get_user_attr_value_list_by_attr_id(object_id_list, attr_id):
        client = global_variables.GLOBAL_CLIENT
        filter_dictionary = {
            'object_id__in': object_id_list,
            'client': client,
            'attribute_id': attr_id
        }
        required_field_list = ['object_id', 'attribute_id', 'low', 'attr_level_default', 'attr_level_exclude',
                               'attr_level_guid']
        org_attr_details = DjangoQueries.django_filter_query(OrgAttributesLevel, filter_dictionary, None,
                                                             required_field_list)

        attr_detail_list = sort_list_dictionary_key_values(object_id_list, org_attr_details, 'object_id')
        org_attr_value_list, org_attr_exclude_details = OrgAttributeValues.get_attr_value_and_exclude_detail(
            attr_detail_list)
        attr_low_value_list, exclude_list = OrgAttributeValues.get_org_attr_values_list(org_attr_value_list,
                                                                                        object_id_list,
                                                                                        org_attr_exclude_details,
                                                                                        attr_detail_list)

        return list(attr_low_value_list)

    @staticmethod
    def get_user_default_attr_value_list_by_attr_id(object_id_list, attr_id):
        client = global_variables.GLOBAL_CLIENT
        filter_dictionary = {
            'object_id__in': object_id_list,
            'client': client,
            'attribute_id': attr_id,
            'del_ind':False
        }
        required_field_list = ['object_id', 'attribute_id', 'low', 'attr_level_default', 'attr_level_exclude',
                               'attr_level_guid']
        org_attr_details = DjangoQueries.django_filter_query(OrgAttributesLevel, filter_dictionary, None,
                                                             required_field_list)

        attr_detail_list = sort_list_dictionary_key_values(object_id_list, org_attr_details, 'object_id')
        org_attr_value_list, org_attr_exclude_details = OrgAttributeValues.get_attr_value_and_exclude_detail(
            attr_detail_list)
        attr_low_value_list, default_attr_list = OrgAttributeValues.get_configured_attr_values_attr_default(
            org_attr_value_list,
            object_id_list,
            org_attr_exclude_details,
            attr_detail_list)

        return attr_low_value_list, default_attr_list
