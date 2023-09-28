class BaseClass:
    def __new__(cls, *args, **kwargs):
        if cls != cls.__base__:
            base_attributes = set(dir(cls.__base__))
            derived_attributes = set(dir(cls))
            new_attributes = derived_attributes - base_attributes

            new_class_attributes = [
                m for m in new_attributes if not callable(getattr(cls, m))
            ]

            new_private_attributes = [
                m
                for m in new_class_attributes
                if m.startswith("_") and not m.startswith("__")
            ]

            new_public_attributes = [
                m for m in new_class_attributes if not m.startswith("_")
            ]

            new_public_methods_attributes = [
                m
                for m in new_attributes
                if callable(getattr(cls, m)) and not m.startswith("_")
            ]
            general_message = "Public or Private Attributes are completely forbidden, as well as new public methods. Use the database to save states."
            if new_private_attributes:
                raise TypeError(
                    f"The derived class '{cls.__name__}' has private class-level attributes not defined in the base class: {', '.join(new_private_attributes)} {general_message}"
                )

            if new_public_attributes:
                raise TypeError(
                    f"The derived class '{cls.__name__}' has public class-level attributes not defined in the base class: {', '.join(new_public_attributes)} {general_message}"
                )

            if new_public_methods_attributes:
                raise TypeError(
                    f"The derived class '{cls.__name__}' has public methods not defined in the base class: {', '.join(new_public_methods_attributes)} {general_message}"
                )

        return super().__new__(cls)
