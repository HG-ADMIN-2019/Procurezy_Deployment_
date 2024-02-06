# # Generates HTML table by Queryset
#
# from django.template import loader
#
#
# class GenTable:
#     """
#     I/P: tbl_model - Model name
#          tbl_clmns - Columns list
#          clmn_fl   - Column flag
#          tbl_data  - Queryset
#          spl_clmns - Columns which are not just for display ( eg: create hyperlink columns )
#     O/P: get_table_data method returns HTML code
#     Behaviour of clmn_fl flag:
#         clmn_fl = None  -> All columns of the table will be displayed
#         clmn_fl = False -> The columns mentioned in tbl_clmns array will be removed
#         clmn_fl = True  -> Only the columns mentioned in tbl_clmns array will be displayed
#     """
#     column_set = []         # Final column set
#     data_set = []           # Final data set
#     link_columns = []       # Special columns
#     tbl_num = None
#
# # Constructor
#     def __init__(self, tbl_model, tbl_clmns, clmn_fl, tbl_data, spl_clmns):
#         self.link_columns = spl_clmns
#         self.column_set = []
#         self.gen_columns(tbl_model, clmn_fl, tbl_clmns)
#         self.data_set = tbl_data
#         self.tbl_num = tbl_model
#
# # Generates column list that needs to be displayed
#     def gen_columns(self, tbl_model, column_flag, tbl_clmns):
#         model_data = tbl_model._meta.concrete_fields
#         for model_column in model_data:
#             if column_flag is None:
#                 self.column_set.append(self.get_clmn_set(model_column.name))
#             elif column_flag is True:
#                 if model_column.name in tbl_clmns:
#                     self.column_set.append(self.get_clmn_set(model_column.name))
#             elif column_flag is False:
#                 if model_column.name not in tbl_clmns:
#                     self.column_set.append(self.get_clmn_set(model_column.name))
#
# # Adds extra information(type) to column to manage spl_clmns
#     def get_clmn_set(self, clmn_name):
#         if not clmn_name in self.link_columns:
#             return clmn_name, 0
#         elif clmn_name == 'sc_num' or clmn_name == 'po_num':
#             return clmn_name, 2
#         else:
#             return clmn_name, 1
#
# # Returns the HTML code
#     def get_table_data(self, req):
#         template = loader.get_template('GETHTML/GenTable/gen_table.html')
#         context = {'column_list': self.column_set, 'data_list': self.data_set, 'tbl_model': self.tbl_num}
#         tmplt = template.render(context, req)
#         return tmplt
