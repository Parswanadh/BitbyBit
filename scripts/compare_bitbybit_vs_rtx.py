#!/usr/bin/env python3
"""Repo-root entry point — delegates to custom_gpu_project implementation."""
import os
import runpy

_ROOT = os.path.dirname(os.path.abspath(__file__))
_TARGET = os.path.join(_ROOT, "..", "custom_gpu_project", "scripts", "compare_bitbybit_vs_rtx.py")
runpy.run_path(_TARGET, run_name="__main__")
