import logging

import traitlets
import traitlets.config
from traitlets import TraitType, TraitError


class Configurable(traitlets.config.Configurable):
    """A (new) Configurable that patches traitlets.Configurable
    objects to allow traits that are iterables with class instances.
    """
    def _load_config(self, cfg, section_names=None, traits=None):
        """Load EventLog traits from a Config object, patching the
        handlers trait in the Config object to avoid deepcopy errors.
        """
        this_class = self.__class__
        my_cfg = self._find_my_config(cfg)
        for name, trait_val in my_cfg.items():
            trait = getattr(this_class, name)
            if hasattr(trait, "_has_instances"):
                # Turn container into a pickeable function
                def get():
                    return trait_val
                my_cfg[name] = get
        # Build a new config object.
        patched_cfg = traitlets.config.Config({this_class.__name__: my_cfg})
        super(Configurable, self)._load_config(patched_cfg, section_names=None, traits=None)


class InstanceContainer(TraitType):
    """A trait that takes a list of logging handlers and converts
    it to a callable that returns that list (thus, making this
    trait pickleable).
    """
    info_text = ""
    _has_instances = True
    _class = None

    def validate_elements(self, obj, value):
        if len(value) > 0:
            # Check that all elements are logging handlers.
            for el in value:
                if isinstance(el, self._class) is False:
                    self.element_error(obj)

    def element_error(self, obj):
        raise TraitError(
            "Elements in the '{}' trait of an {} instance "
            "must be instances of {}."
            .format(self.name, obj.__class__.__name__, self._class)
        )

    def validate(self, obj, value):
        # If given a callable, call it and set the
        # value of this trait to the returned list.
        # Verify that the callable returns a list
        # of logging handler instances.
        if callable(value):
            out = value()
            self.validate_elements(obj, out)
            return out
        # If a list, check it's elements to verify
        # that each element is a logging handler instance.
        elif type(value) == list:
            self.validate_elements(obj, value)
            return value
        else:
            self.error(obj, value)
