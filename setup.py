from __future__ import annotations

import os
from pathlib import Path

from setuptools import find_namespace_packages, find_packages, setup

NAME = "geco2"
VERSION = "0.1.0"
DESCRIPTION = "Generalized-scale few-shot object counting and detection"
URL = "https://github.com/jerpelhan/GECO2"
AUTHOR = "Jer Pelhan"
LICENSE = "MIT"
ROOT = Path(__file__).parent.resolve()
README = (ROOT / "README.md").read_text(encoding="utf-8")

BUILD_CUDA = os.getenv("GECO2_BUILD_CUDA", "1") == "1"
BUILD_ALLOW_ERRORS = os.getenv("GECO2_BUILD_ALLOW_ERRORS", "1") == "1"
CUDA_ERROR_MSG = (
    "{}\n\n"
    "Failed to build the optional MultiScaleDeformableAttention extension. "
    "GECO2 will still install and will fall back to the PyTorch implementation, "
    "but attention layers will run more slowly.\n"
)


def get_packages() -> list[str]:
    regular_packages = find_packages(include=["configs*", "geco2*", "models*", "utils*"])
    namespace_packages = find_namespace_packages(include=["sam2", "sam2.*"])
    return sorted(set(regular_packages + namespace_packages))


def get_extensions():
    if not BUILD_CUDA:
        return []

    try:
        import torch
        from torch.utils.cpp_extension import CUDAExtension

        extensions_dir = ROOT / "Deformable-DETR" / "models" / "ops" / "src"
        sources = [
            extensions_dir / "vision.cpp",
            extensions_dir / "cpu" / "ms_deform_attn_cpu.cpp",
            extensions_dir / "cuda" / "ms_deform_attn_cuda.cu",
        ]
        extra_compile_args = {
            "cxx": [],
            "nvcc": [
                "-DCUDA_HAS_FP16=1",
                "-D__CUDA_NO_HALF_OPERATORS__",
                "-D__CUDA_NO_HALF_CONVERSIONS__",
                "-D__CUDA_NO_HALF2_OPERATORS__",
            ],
        }
        return [
            CUDAExtension(
                "MultiScaleDeformableAttention",
                [str(source) for source in sources],
                include_dirs=[str(extensions_dir)],
                define_macros=[("WITH_CUDA", None)],
                extra_compile_args=extra_compile_args,
            )
        ]
    except Exception as exc:
        if BUILD_ALLOW_ERRORS:
            print(CUDA_ERROR_MSG.format(exc))
            return []
        raise


try:
    from torch.utils.cpp_extension import BuildExtension

    class BuildExtensionIgnoreErrors(BuildExtension):
        def finalize_options(self):
            try:
                super().finalize_options()
            except Exception as exc:
                print(CUDA_ERROR_MSG.format(exc))
                self.extensions = []

        def build_extensions(self):
            try:
                super().build_extensions()
            except Exception as exc:
                print(CUDA_ERROR_MSG.format(exc))
                self.extensions = []

        def get_ext_filename(self, ext_name):
            try:
                return super().get_ext_filename(ext_name)
            except Exception as exc:
                print(CUDA_ERROR_MSG.format(exc))
                self.extensions = []
                return "MultiScaleDeformableAttention.so"

    cmdclass = {
        "build_ext": (
            BuildExtensionIgnoreErrors.with_options(no_python_abi_suffix=True)
            if BUILD_ALLOW_ERRORS
            else BuildExtension.with_options(no_python_abi_suffix=True)
        )
    }
except Exception as exc:
    cmdclass = {}
    if BUILD_ALLOW_ERRORS:
        print(CUDA_ERROR_MSG.format(exc))
    else:
        raise


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    license=LICENSE,
    packages=get_packages(),
    include_package_data=True,
    package_data={
        "configs": ["*.yaml"],
        "sam2.sam2_configs": ["*.yaml"],
    },
    python_requires=">=3.10",
    install_requires=[
        "hydra-core>=1.3.2",
        "numpy<2",
        "omegaconf>=2.3.0",
        "pillow>=9.4.0",
        "pycocotools>=2.0.8",
        "scikit-image>=0.22.0",
        "scipy>=1.11.0",
        "torch>=2.3.1",
        "torchvision>=0.18.1",
        "tqdm>=4.66.1",
    ],
    extras_require={
        "demo": [
            "gradio>=4.44.1",
            "gradio-image-prompter>=0.1.0",
            "matplotlib>=3.8.0",
        ],
        "eval": [
            "fvcore>=0.1.5.post20221221",
            "opencv-python>=4.8.0",
            "tabulate>=0.9.0",
        ],
    },
    ext_modules=get_extensions(),
    cmdclass=cmdclass,
    license_files=["LICENSE"],
    zip_safe=False,
)
