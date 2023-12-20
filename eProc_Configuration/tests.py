from django.test import TestCase

# Create your tests here.

# guid = request.POST.getlist('guid[]')
#     for edit_nr in conf_num_range:
#         if int(st_num) in range(int(edit_nr.starting), int(edit_nr.ending)):
#             return JsonResponse({'message': 'Number ranges conflict with others'}, status=400)
#         if int(end_num) in range(int(edit_nr.starting), int(edit_nr.ending)):
#             return JsonResponse({'message': 'Number ranges conflict with others'}, status=400)
#     if NumberRanges.objects.filter(sequence=seq, client=getClients(request)).exists():
#         return JsonResponse({'message': 'Sequence ' + seq + ' already in use'}, status=400)
#     if NumberRanges.objects.filter(starting=st_num, client=getClients(request)).exists():
#         return JsonResponse({'message': 'Starting number ' + st_num + ' already in use'}, status=400)
#     if NumberRanges.objects.filter(ending=end_num, client=getClients(request)).exists():
#         return JsonResponse({'message': 'Ending number ' + end_num + ' already in use'}, status=400)
#     if NumberRanges.objects.filter(current=cur, client=getClients(request)).exists():
#         return JsonResponse({'message': 'Current number ' + seq + ' already in use'}, status=400)
#     edit_num_range = NumberRanges.objects.filter(guid=guids, client=getClients(request))
#     edit_num_range.update(sequence=seq, starting=st_num, ending=end_num, current=cur)