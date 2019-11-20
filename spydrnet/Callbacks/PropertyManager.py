


class Callback:

    def __init__(self):
        #the functions to run before the function call is made
        self._before = []
        #the functions to run after the function call is made
        self._after = []

    def register_before(self, function):
        '''
        register a function to be run when run_after is called.
        parameters:
        function - the function that will be registered. it should accept *args that match the function that is to be surrounded by callbacks
        '''
        self._before.append(function)

    def register_after(self, function):
        '''
        register a function to be run when run_after is called.
        parameters:
        function - the function that will be registered. it should accept *args that match the function that is to be surrounded by callbacks
        '''
        self._after.append(function)

    def run_before(self,*args):
        '''
        run all the functions that are registered as before passing them the *args that are passed in here
        '''
        for f in self._before:
            f(*args)
        
    def run_after(self,*args):
        '''
        run all the functions that are registered as before passing them the *args that are passed in here
        '''
        for f in self._after:
            f(*args)