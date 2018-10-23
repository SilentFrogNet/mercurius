import abc
import importlib
import os
import pluggy

from mercurius.utils import get_project_path


class PluginLoader:
    __metaclass__ = abc.ABCMeta

    DEFAULT_PLUGINS_PATH = None  # To be defined in the inherited class
    DEFAULT_PLUGINS_PACKAGE = None  # To be defined in the inherited class

    def __init__(self, project_name, project_spec, configs, plugin_path=DEFAULT_PLUGINS_PATH, plugin_package=DEFAULT_PLUGINS_PACKAGE):
        self.plugin_path = plugin_path
        self.plugin_package = plugin_package
        self.configs = configs

        # create a manager and add the spec
        self.project_name = project_name
        self.project_spec = project_spec
        self.pm = pluggy.PluginManager(self.project_name)
        self.pm.add_hookspecs(self.project_spec)

    def register_plugins(self, logger=None):
        allowed_plugins = self.get_enabled_plugins()

        script_path = get_project_path()
        plugin_path = os.path.join(script_path, self.plugin_path)

        for d in os.listdir(plugin_path):
            full_path = os.path.join(plugin_path, d)
            if os.path.isfile(full_path) and d != "__init__.py":
                plugin_name = os.path.splitext(d)[0]
                class_name = allowed_plugins.get(plugin_name, None)
                if class_name:
                    plugin_name = ".{}".format(plugin_name)
                    mod = importlib.import_module(plugin_name, self.plugin_package)
                    klass = getattr(mod, class_name)(logger)
                    self.pm.register(klass)

    @abc.abstractmethod
    def get_enabled_plugins(self):
        raise NotImplementedError('Not yet implemented')

    def get_plugin_manager(self):
        return self.pm
