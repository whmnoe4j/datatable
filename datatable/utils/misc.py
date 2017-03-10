#!/usr/bin/env python
# Copyright 2017 H2O.ai; Apache License Version 2.0;  -*- encoding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__all__ = ("clamp", "normalize_slice", "plural_form")


def plural_form(n, singular, plural=None):
    if n == 1 or n == -1:
        return "%d %s" % (n, singular)
    else:
        if not plural:
            last_letter = singular[-1]
            prev_letter = singular[-2] if len(singular) >= 2 else ""
            if last_letter == "s" or last_letter == "x":
                plural = singular + "es"
            elif last_letter == "y":
                plural = singular[:-1] + "ies"
            elif last_letter == "f" and prev_letter != "f":
                plural = singular[:-1] + "ves"
            elif last_letter == "e" and prev_letter == "f":
                plural = singular[:-2] + "ves"
            elif last_letter == "h" and prev_letter in "sc":
                # Note: words ending in 'ch' which is pronounced as /k/
                # are exception to this rule: monarch -> monarchs
                plural = singular + "es"
            else:
                plural = singular + "s"
        return "%d %s" % (n, plural)


def clamp(x, lb, ub):
    """Return the value of ``x`` clamped to the range ``[lb, ub]``."""
    return min(max(x, lb), ub)


def normalize_slice(e, n):
    """
    Return the slice tuple normalized for an ``n``-element object.

    :param e: a slice or range object representing a selector
    :param n: number of elements in a sequence to which ``e`` is applied
    :returns: tuple ``(start, count, step)`` derived from ``e``.
    """
    if n == 0:
        return (0, 0, 0)

    step = e.step
    if step is None or step == 0:
        step = 1
    assert isinstance(step, int) and step != 0

    start = None
    if e.start is None:
        start = 0 if step > 0 else n - 1
    else:
        start = e.start
        if start < 0:
            start += n
        if (start < 0 and step < 0) or (start >= n and step > 0):
            return (0, 0, 0)
        start = min(max(0, start), n - 1)
    assert isinstance(start, int) and 0 <= start < n, \
        "Invalid start: %r" % start

    count = None
    if e.stop is None:
        if step > 0:
            count = (n - 1 - start) // step + 1
        else:
            count = (start // -step) + 1
    else:
        stop = e.stop
        if stop < 0:
            stop += n
        if step > 0:
            if stop > start:
                count = (min(n, stop) - 1 - start) // step + 1
            else:
                count = 0
        else:
            if stop < start:
                count = (start - max(stop, -1) - 1) // -step + 1
            else:
                count = 0
    assert isinstance(count, int) and count >= 0
    assert count == 0 or 0 <= start + step * (count - 1) < n, \
        "Wrong tuple: (%d, %d, %d)" % (start, count, step)

    return (start, count, step)