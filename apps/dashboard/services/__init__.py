# apps/dashboard/services/__init__.py
from .docx_builder import build_sitrep_docx
from .wa_formatter import format_wa_sitrep

__all__ = ["build_sitrep_docx", "format_wa_sitrep"]
