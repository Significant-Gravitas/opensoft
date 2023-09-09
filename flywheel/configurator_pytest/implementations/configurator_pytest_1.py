import glob
import importlib
import os
import pkgutil
from typing import List, Dict, Tuple

from flywheel.configurator_pytest.abstract_class import AbstractConfiguratorPytest


class ConfiguratorPytest1(AbstractConfiguratorPytest):

    def setup_parameterization(self, metafunc):
        script_folder = os.path.dirname(str(metafunc.definition.fspath))
        script_folder_relative = os.path.relpath(script_folder, os.getcwd())
        script_folder_parent_relative = os.path.dirname(script_folder_relative)
        # folder = metafunc.config.args[0] if metafunc.config.args and metafunc.config.args[0].split("/")[-1] != "flywheel" else script_folder_parent_relative

        module, to_parameterize = self._prepare_for_parameterization(metafunc, script_folder_parent_relative)

        return module, to_parameterize

    def _prepare_for_parameterization(self, metafunc, folder) -> Tuple[str, List[type]]:
        # Discover implementations
        implementations = self._discover_implementations(folder)

        # Get implementation option and determine parameterization
        implementation_option = metafunc.config.option.implementation
        to_parameterize = self._determine_parameterization(implementations, implementation_option)

        # Determine module name for parameterization
        module = folder.split('/')[-1]

        return module, to_parameterize

    def _convert_to_camel_case(self, s: str) -> str:
        parts = s.split('_')
        return ''.join(part.capitalize() for part in parts)

    def _discover_implementations(self, folder: str) -> Dict[str, type]:
        implementations = {}
        for package_name in glob.glob(f'{folder}/implementations'):
            package_path = package_name.replace('/', '.')
            package = importlib.import_module(package_path)
            for _, module_name, _ in pkgutil.iter_modules(package.__path__):
                full_module_name = f"{package_path}.{module_name}"
                module = importlib.import_module(full_module_name)
                class_name = self._convert_to_camel_case(module_name)
                try:
                    class_ = getattr(module, class_name)
                except AttributeError:
                    continue
                implementations[module_name] = class_
        return implementations

    def _determine_parameterization(self, implementations: Dict[str, type], option: str) -> List[type]:
        if option in implementations:
            return [implementations[option]]
        else:
            return list(implementations.values())
