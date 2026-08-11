
"""
Field validation helper.

Place a held-out FIELD dataset under:
field_eval/<class_name>/*.jpg

Run:
  python evaluate.py

This is intentionally separate from the training dataset to prevent
benchmark leakage and to demonstrate field robustness to judges.
"""
import os, json
print("Field evaluation scaffold ready.")
print("Create field_eval/ with independently captured field images.")
print("Report per-class precision/recall and a confusion matrix.")
