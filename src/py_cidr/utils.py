'''
Dev tools
'''
def print_dictionary(dic, indent=0):
    '''
    simple dictionary printer
    Used to dump cidr cache 
    '''
    for (key, val) in dic.items():
        if isinstance(val, dict):
            print(' ' * indent + str(key) + ':')
            print_dictionary(val, indent + 2)
        else:
            print(' ' * indent + str(key) + ': ' + str(val))
