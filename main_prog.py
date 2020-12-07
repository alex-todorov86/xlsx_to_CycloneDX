from sys import argv
import pandas as pd
import json


##################################
#        FUNCTIONS BLOCK         #
##################################


def args_to_kwargs(args_list):
    '''
    Converts args to kwargs.
    An arg is considered as kwarg
    when it's preceeded with a dash (-)
    '''
    out = {}
    for i in range(1, len(args_list)):
        if args_list[i].startswith('-'):
            out[args_list[i]] = args_list[i+1]
    return out

#print(args_to_kwargs(argv))
