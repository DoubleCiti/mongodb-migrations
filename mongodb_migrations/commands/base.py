from mongodb_migrations.config import Configuration


class Base(object):
    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.config = Configuration(options, args, kwargs)

    def run(self):
        raise NotImplementedError('run() method not implemented')

    def check_required_args(self, requered_args):
        requered_args = set(requered_args)
        args = set([x for x in dir(self.config) if not x.startswith("_")
                    and self.config.__getattribute__(x) is not None])
        left_args = requered_args - args
        if left_args:
            print("%s arguments are required" % list(left_args))
            exit(1)
