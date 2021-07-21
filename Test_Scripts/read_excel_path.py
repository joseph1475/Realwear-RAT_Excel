import click
import subprocess


@click.command()
@click.option('--excel', default='', help='Excel path to be run')
def path_getter(excel):
    print('##########')
    print(excel)
    return excel

