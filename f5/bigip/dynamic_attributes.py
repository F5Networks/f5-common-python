class LazyAttributeMixin(object):
    def __getattr__(self, name):
        for lazy_attribute in self.allowed_lazy_attributes:
            if name == lazy_attribute.__name__.lower():
                iface_collection = lazy_attribute(self)
                setattr(self, name, iface_collection)
                return iface_collection
        error_message = "'%s' object has no attribute '%s'"\
            % (self.__class__, name)
        raise AttributeError(error_message)
