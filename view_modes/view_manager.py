class ViewManager:
    def __init__(self):
        self.__registered_views = dict()

    def register(self, view_name, fconstructor):
        self.__registered_views[view_name] = fconstructor

    def createview(self, view_name):
        return self.__registered_views[view_name]()
