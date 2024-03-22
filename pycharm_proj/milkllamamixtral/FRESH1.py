import argparse
import sys

class MilkitCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="THE 1 PURPOSE
CLI TO CREATE CUSTOM PROMPTING AND COMMAND FUNCTION TEMPLATES! ALL IT DOES
IS MILK!")
        self.subparsers = self.parser.add_subparsers(dest='command')

    def add_milk_commands(self, parent_parser):
        milk_parser = parent_parser.add_parser('milk', help="Command
prefix for function creation")
        uttr_parser = milk_parser.add_parser('uttr', help="Aliases for
'print or prompt to user' CLI commands")
        uttr_parser.add_argument('title', help="Add a new 'uttr' command
variable")
        uttr_parser.add_argument('cow', help="The body of text that is
printed to the user")

    def add_bucket_commands(self, parent_parser):
        bucket_parser = parent_parser.add_parser('bucket', help="Display
the current cued CLI prompting to the user")

    def add_bag_commands(self, parent_parser):
        bag_parser = parent_parser.add_parser('bag', help="A universal
'save' command")

    def add_bottle_commands(self, parent_parser):
        bottle_parser = parent_parser.add_parser('bottle', help="Create
placeholders for Python command functions in proper syntax with the
prompting user created in uttr step.")

    def add_fridge_commands(self, parent_parser):
        fridge_parser = parent_parser.add_parser('fridge', help="'milkit'
CLI home screen command")
        fridge_parser.set_defaults(func=self.handle_fridge_command)

    def handle_fridge_command(self, args):
        if args.subcommand == 'milkit':
            print("Help for milkit commands")
        elif args.subcommand == 'uttr':
            print("List all uttr commands")
        elif args.subcommand == 'bucket':
            print("Display the current prompting print for the user,
built-in the CLI.")

    def parse_args(self):
        self.args = self.parser.parse_args()

if __name__ == "__main__":
    milkit_cli = MilkitCLI()
    milkit_cli.add_milk_commands(milkit_cli.subparsers)
    milkit_cli.add_bucket_commands(milkit_cli.subparsers)
    milkit_cli.add_bag_commands(milkit_cli.subparsers)
    milkit_cli.add_bottle_commands(milkit_cli.subparsers)
    milkit_cli.add_fridge_commands(milkit_cli.subparsers)
    milkit_cli.parse_args()