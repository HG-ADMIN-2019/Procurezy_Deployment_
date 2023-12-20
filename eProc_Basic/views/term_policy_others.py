import copy

from django.shortcuts import render


def private_policies(request):
    """

    """
    return render(request, 'root/privacy_policy.html')


def terms_of_use(request):
    """

    """
    return render(request, 'root/terms_of_use.html')


def remove_duplicates(arr):
    # Convert each row to a tuple
    tuple_array = [tuple(row) for row in arr]

    # Create a set of tuples to eliminate duplicates
    unique_tuples = set(tuple_array)

    # Convert the set back to a list of lists
    result = [list(row) for row in unique_tuples]

    return result


def remove_duplicate_paytermdesc(arr):
    # Create a deep copy of each row as a tuple
    tuple_array = [tuple(copy.deepcopy(row)) for row in arr]

    # Create a set of tuples to eliminate duplicates
    unique_tuples = set(tuple_array)

    # Convert the set back to a list of lists
    result = [list(row) for row in unique_tuples]

    return result
