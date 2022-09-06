from os.path import dirname, realpath

from dynaconf import LazySettings

_file_dirname: str = dirname(realpath(__file__))


config: LazySettings = LazySettings(ROOT_PATH_FOR_DYNACONF=_file_dirname,
                                    SETTINGS_FILE_FOR_DYNACONF="default_config.yaml",
                                    INCLUDES_FOR_DYNACONF="config.yaml",
                                    MERGE_ENABLED_FOR_DYNACONF=True,
                                    CORE_LOADERS_FOR_DYNACONF=["YAML"])
