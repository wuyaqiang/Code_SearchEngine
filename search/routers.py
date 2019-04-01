
from haystack import routers

class ProblemRouter(routers.BaseRouter):
    def for_write(self,**hints):
        return 'problem'
        # return None

    def for_read(self,**hints):
        # return None
        return 'problem'


class ProblemCodeRouter(routers.BaseRouter):
    def for_write(self, **hints):
        # return None
        return 'problemcode'

    def for_read(self, **hints):
        return 'problemcode'

class QuestionRouter(routers.BaseRouter):
    def for_write(self,**hints):
        # return None
        return 'question'

    def for_read(self,**hints):
        return 'question'