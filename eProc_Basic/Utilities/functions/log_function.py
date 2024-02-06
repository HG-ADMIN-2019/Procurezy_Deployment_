from eProc_Basic.Utilities.global_defination import global_variables


def update_log_info(created_at_val, created_by_val):
    if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
        changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
        created_by_val = created_by_val[0]
    else:
        changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
        created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

    result = {'created_by_val': created_by_val, 'changed_by_val': changed_by_val}
    return result
