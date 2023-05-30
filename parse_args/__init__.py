__all__ = ["arg", "usage"]


import sys
from argparse import ArgumentParser


def arg(*ap_args, **ap_kwargs):
    return lambda fn: _wrap(fn, ap_args=ap_args, ap_kwargs=ap_kwargs)


def usage(_usage):
    return lambda fn: _wrap(fn, usage=_usage)


def _wrap(fn, *, usage=None, ap_args=None, ap_kwargs=None):
    if isinstance(fn, _functionWrapper):
        if usage:
            fn.parser.usage = usage
        else:
            fn.parser.add_argument(*ap_args, **ap_kwargs)
        return fn
    return _functionWrapper(fn, usage=usage, ap_args=ap_args, ap_kwargs=ap_kwargs)


class _functionWrapper:

    def __init__(self, fn, *, usage=None, ap_args=None, ap_kwargs=None):
        self.fn = fn
        self.parser = ArgumentParser(usage=usage)
        if ap_args or ap_kwargs:
            self.parser.add_argument(*ap_args, **ap_kwargs)

    def __call__(self, argv=None):
        if argv is None:
            argv = sys.argv[1:]
        args = self.parser.parse_args(argv)
        return self.fn(args)

