__all__ = ["build_inference_model", "build_training_model", "get_argparser"]


def build_training_model(*args, **kwargs):
	from models.counter import build_model

	return build_model(*args, **kwargs)


def build_inference_model(*args, **kwargs):
	from models.counter_infer import build_model

	return build_model(*args, **kwargs)


def get_argparser(*args, **kwargs):
	from utils.arg_parser import get_argparser as _get_argparser

	return _get_argparser(*args, **kwargs)
