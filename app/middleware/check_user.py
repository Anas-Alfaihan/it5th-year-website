class CheckUser(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path)
        if '/app/upload/' in request.path:
            print('warning')
            #send warning
            # if request.user.is_authenticated and not request.user.lastPull.waitingMerge:
            #     raise Exception('You must first push data to pull current data.')
        else:
            if request.user.is_authenticated and request.user.lastPull.waitingMerge:
                raise Exception('Your last pull request is waiting for a merge. Please try again later.')
        response = self.get_response(request)

        return response

    
   