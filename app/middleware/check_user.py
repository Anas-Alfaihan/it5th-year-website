from django.contrib import messages
from django.shortcuts import redirect, render
from app.forms import UploadFileForm
from django.contrib.auth.models import User
from django.http import JsonResponse

class CheckUser(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if User.objects.filter().count() == 0 and '/app/firstUpload/' not in request.path:
            return redirect('app:first_upload_file')
        elif '/app/upload/' in request.path:
            #send warning
            if request.user.is_authenticated and not request.user.lastPull.waitingMerge:
                messages.add_message(request, messages.WARNING,"إذا تم دمج تحديثات نسخة الأونلاين فسيتم حذف جميع الإضافات غير المسحوبة , لكن ستبقى التعديلات والحذف الذي طبق متاحاً للسحب")
        elif not '/app/download/' in request.path:
            if request.user.is_authenticated and request.user.lastPull.waitingMerge and request.method=='POST':
                
                if '/app/updateDispatch/' in request.path or '/app/updateExtension/' in request.path or '/app/updateFreeze/' in request.path or '/app/updateUnv/' in request.path or '/app/updateGrad/' in request.path or '/app/updateDemon/' in request.path:
                    return JsonResponse({"status": "عليك جلب التحديثات من نسخة الأونلاين"})
                else:
                    messages.add_message(request, messages.ERROR,"عليك جلب التحديثات من نسخة الأونلاين")
                    return redirect(request.META.get('HTTP_REFERER'))
        response = self.get_response(request)

        return response

    
   