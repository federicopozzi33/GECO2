from hydra import initialize_config_module
from hydra.core.global_hydra import GlobalHydra


if not GlobalHydra.instance().is_initialized():
	initialize_config_module("configs", version_base="1.2")