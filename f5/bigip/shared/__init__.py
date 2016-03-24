from f5.bigip.resource import PathElement
from f5.bigip.shared.licensing import Licensing


class Shared(PathElement):
    def __init__(self, bigip):
        super(Shared, self).__init__(bigip)
        self._meta_data['allowed_lazy_attributes'] = [Licensing]
