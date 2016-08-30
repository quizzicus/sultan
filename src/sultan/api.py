from .core import Base

def shell_decorator(name):

    pass

class Sultan(Base):

    commands = []

    def __getattr__(self, name):

        return Command(self, name)

    def __shell_call(self, name, *args, **kwargs):

        return { "args": args, "kwargs": kwargs }

    def add(self, command):

        self.commands.append(command)

    def clear(self):

        del self.commands[:]
        return self

    def __str__(self):

        return " ".join([str(c) for c in self.commands])

class Command(Base):

    command = None
    args = []
    kwargs = {}

    def __init__(self, sultan, name):

        self.sultan = sultan
        self.command = name

    def __call__(self, *args, **kwargs):

        if len(kwargs) == 0 and len(args) == 1 and type(args[0]) == str:
            self.args = args[0].split(" ")
            self.sultan.add(self)
        else:
            self.args = args
            self.kwargs = kwargs
            self.sultan.add(self)
        return self.sultan

    def __str__(self):

        args_str = (" ".join(self.args)).strip()
        kwargs_list = []
        for k, v in self.kwargs.iteritems():

            key = None
            value = v
            if len(k) == 1:
                key = "-%s" % k
            else:
                key = "--%s" % k
            kwargs_list.append("%s=%s" % (key, value))
        kwargs_str = " ".join(kwargs_list).strip()

        # prep and return the output
        output = self.command
        if len(kwargs_str) > 0: output = output + " " + kwargs_str
        if len(args_str) > 0: output = output + " " + args_str
        return output

class Pipe(Command):

    def __call__(self):

        self.command = "|"

    def __str__(self):
        return "|"
