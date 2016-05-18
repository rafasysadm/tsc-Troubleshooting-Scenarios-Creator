from subprocess import call, Popen


import click
import sys
import os
import re

import logging
import traceback


from platform import dist # check Linux distribution
script_dir = os.path.dirname(__file__) + "/scenarios/"
#print (script_dir)

def validate_pr(problem):
    distro = dist()[0]
    # scenario_run = [ i for i in os.listdir(script_dir)
    #                    for pr in problem
    #                    if pr == i.split(".")[0] ] 


    scenario_run = []
    non_existent = []
    dir_files = os.listdir(script_dir)
    #print(dir_files)

    nl = { i.split(".")[0]:i for i in dir_files }
    #non_existent = [ i for i in dir_files if i not in nl ]
    #print(nl)
    #print(problem)
# this is shitty code. Fix it to compare in a reliable way.
    for pr in problem:
        if pr in nl.keys():
            scenario_run.append(nl[pr])
        else:
            non_existent.append(pr)

    return scenario_run, non_existent

def organizer(problem):
    distro = dist()[0].lower()
    scenario_run, non_existent = validate_pr(problem)

    # scenario_run = [ i for i in os.listdir(script_dir)
    #                    for pr in problem
    #                    if pr == i.split(".")[0] ]

    scn_validated = []

    if non_existent:
        click.secho("--- Scenario(s) not found: %s"   % " ".join(non_existent), err=True, blink=True, bold=True, fg="yellow")

    for scn in scenario_run:
        with open(script_dir + scn, 'r') as f:
            lines = f.read()
            distrib = re.search("OS\s*=\s*[\"\']?\w+[\"\']?", lines, re.MULTILINE)
            if distrib is None:
                click.secho("\n --- %s is not compatible with %s. Feel free to contribute making a proper plugin for that.\n" %( scn, distro), err=True, fg="yellow")
               # print(distrib)
                continue
            else:
                #print(distrib)
                distrib = distrib.group().split("=")[1].lower()
                distrib = re.sub(r'[\s*\"\']|[\s*\"\']$', '', distrib) #distrib.group().split("=")[1]
                #print(distrib)
                if distrib == distro:
                    #print ("xxx", distrib)
                    scn_validated.append(scn)
                else:
                   # print(distrib)
                    click.secho("\n --- %s is not compatible with %s. Feel free to contribute making a proper plugin for that.\n" %( scn, distro), err=True, fg="yellow")  
    return scn_validated


# Creates a group, so we can nest the commands.
@click.group()
def tbs_cli():
    pass

@tbs_cli.command()
@click.option('--problem', '-p',
            multiple=True, 
            help='Troubleshooting scenario to be loaded.'
             )

#@click.option('--distro', default=dist()[0], help='Choose the OS to load the Troubleshooting scenarios.')
def runit(problem):
    """Run Troubleshooting scenarios."""
    scenarios = "\n".join(problem)
    scenario_run = (organizer(problem))

    click.secho("FixIT is starting. The chosen scenario(s) will be loaded.\n", fg="green")
    click.secho("Warning: If you are remotelly connected, your connection may be dropped depending on the scenario you have chosen.\n", fg="red")

    for scn in scenario_run:
        click.secho("--- %s: Starting.\n" %scn, fg="green")                  
        try:
            retcode = call(script_dir + scn)
            #retcode = Popen([script_dir, scn], shell=True)
            # print(retcode)
            # #print(scn)
            # if retcode > 0:
            #     raise 

                #print("Scenario %s failed to load." % problem, retcode)
        except Exception as e:
            # click.echo("Scenario %s failed to load." % scn, e)
            # click.echo("Execution failed:", e, file=sys.stderr)
            #logging.error(traceback.format_exc())
            click.secho(sys.exc_info()[1], err=True, fg="yellow")
            click.secho("%s has failed to execute. Please, check plugins permissions.\n" % scn, err=True, fg="yellow")
        # except:
        #     click.echo("Execution failed::", sys.exc_info()[0])
        else:
            click.secho("Scenario %s successfully loaded\n" % scn, fg="green")
            #click.echo("-----------------------------------------")


#tbs_cli.add_command(runit(problem))

# CRIAR FUNC PARA USAR DENTRO DE runit

#@click.option('--location', default="local", help='The person to greet.')

#def distro(distro=dist()[0]):
    #get to specific directory to distro.
    #pass

# Criar clean-up function to remove dupplicate scripts
# manter por default o script em python e/ou o mais novo.