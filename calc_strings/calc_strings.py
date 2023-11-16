# THIS SCRIPT IS A SHORT EXAMPLE ON HOW TO CALCULATE STRING LENGTH FOR LABEL FILES.

from utils.str_calc import calculate, loadKey

loadKey()
print(str(calculate("A hot drink which is good for quenching thirst.")))
print(str(calculate("For linked battles, you may choose which")))
print(str(calculate("set of rules you wish to use.")))
