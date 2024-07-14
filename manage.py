#!/usr/bin/env python3

import argparse
import os
from invoke import Context

def load_commands(parser):
    commands = {}
    command_dir = os.path.join(os.path.dirname(__file__), "app", "commands")
    for file in os.listdir(command_dir):
        if file.endswith('.py') and file != '__init__.py':
            module_name = file[:-3]
            module = __import__(f'app.commands.{module_name}', fromlist=['run'])
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and "__" in attr_name:
                    cmd_name = attr_name.replace("__", ":")
                    func_parser = parser.add_parser(cmd_name, help=attr.__doc__)
                    if hasattr(attr, 'args'):
                        for arg_name, arg_opts in attr.args:
                            func_parser.add_argument(arg_name, **arg_opts)
                    func_parser.set_defaults(func=attr)

    return commands
            

def main():
    parser = argparse.ArgumentParser(description="Manage Flask application commands")
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    load_commands(subparsers)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        ctx = Context()
        func_args = {k: v for k, v in vars(args).items() if k not in ['func', 'command']}
        args.func(ctx, **func_args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
