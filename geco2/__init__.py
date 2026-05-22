__all__ = ["build_inference_model", "build_training_model", "get_argparser"]
__version__ = "0.1.0"


def __getattr__(name):
	if name in __all__:
		from .api import build_inference_model, build_training_model, get_argparser

		return {
			"build_inference_model": build_inference_model,
			"build_training_model": build_training_model,
			"get_argparser": get_argparser,
		}[name]
	raise AttributeError(f"module 'geco2' has no attribute {name!r}")
