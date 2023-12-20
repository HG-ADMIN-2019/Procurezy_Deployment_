from eProc_Attributes.Utilities.attributes_specific import append_attribute_value_description, \
    append_description_atrr_value_exists
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.insert_remove import dictionary_remove_insert_first
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import UnspscCategoriesCust, UnspscCategoriesCustDesc

django_query_instance = DjangoQueries()


class AppendIdDesc:
    @staticmethod
    def query_append_id_desc(db_name, filter_dictionary, field_id, field_desc,default_id):
        """

        """
        django_query_set_result = django_query_instance.django_filter_query(db_name,
                                                                            filter_dictionary,
                                                                            None,
                                                                            [field_id, field_desc])
        django_query_set_result = dictionary_remove_insert_first(django_query_set_result,field_id,default_id)
        append_id_desc = append_attribute_value_description(django_query_set_result, field_id, field_desc)[0]

        return append_id_desc

    @staticmethod
    def query_append_id_desc_language(db_name, filter_dictionary,language_filter, field_id, field_desc, default_id):
        """

        """
        django_query_id_list = django_query_instance.django_filter_value_list_ordered_by_distinct_query(db_name,
                                                                                                        filter_dictionary,
                                                                                                        field_id,
                                                                                                        [field_id])
        django_query_set_result = django_query_instance.django_filter_query(db_name,
                                                                            language_filter,
                                                                            None,
                                                                            [field_id, field_desc])
        django_query_set_result = dictionary_remove_insert_first(django_query_set_result, field_id, default_id)
        append_id_desc = append_description_atrr_value_exists(django_query_set_result,django_query_id_list, field_id, field_desc)[0]

        return append_id_desc



