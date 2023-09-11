class BaseClass:
    def __new__(cls, *args, **kwargs):
        if cls != cls.__base__:
            base_attributes = set(dir(cls.__base__))
            derived_attributes = set(dir(cls))
            new_attributes = derived_attributes - base_attributes

            # Separate methods and non-method attributes
            new_class_attributes = [m for m in new_attributes if not callable(getattr(cls, m))]

            # Filter out new private attributes (those starting with an underscore but not double underscores)
            new_private_attributes = [m for m in new_class_attributes if m.startswith('_') and not m.startswith('__')]

            # Filter out new public methods and attributes
            new_public_methods_attributes = [m for m in new_attributes if not m.startswith('_')]

            if new_private_attributes:
                raise TypeError(f"The derived class '{cls.__name__}' has private class-level attributes not defined in the base class: {', '.join(new_private_attributes)}")

            if new_public_methods_attributes:
                raise TypeError(f"The derived class '{cls.__name__}' has public methods or attributes not defined in the base class: {', '.join(new_public_methods_attributes)}")

        return super().__new__(cls)
