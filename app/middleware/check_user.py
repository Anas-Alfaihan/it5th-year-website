from django.contrib import messages
from django.shortcuts import redirect

class CheckUser(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/app/upload/' in request.path:
            #send warning
            if request.user.is_authenticated and not request.user.lastPull.waitingMerge:
                messages.add_message(request, messages.WARNING,"إذا تم دمج تحديثات نسخة الأونلاين فسيتم حذف جميع التعديلات غير المسحوبة")
        else:
            if request.user.is_authenticated and request.user.lastPull.waitingMerge and request.method=='POST':
                messages.add_message(request, messages.ERROR,"عليك جلب التحديثات من نسخة الأونلاين")
                return redirect(request.META.get('HTTP_REFERER'))
        response = self.get_response(request)

        return response

    
   