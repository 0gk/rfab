import random
import string

from rmodels import Plant, Jbod, Slot

JBODS_PER_PLANT = 5
SLOTS_PER_JBOD = 16 


def slotgen(i: int) -> Slot:
    return Slot(
        idx = i,
        state = Slot.State.ACTIVE,
        status = 'Some status information',
        scode = Slot.Statuscode.OK,
        progress = random.randint(100, 10000),
        mdl = 'MD' + ''.join((random.choice(string.ascii_uppercase) for i in range(4))) + ''.join((random.choice(string.digits) for i in range(20))),
        sn = ''.join((random.choice(string.hexdigits) for i in range(20))),
        itf = Slot.Interface.SAS,
        link = 100500,
        grade = Slot.Grade.HIGH,
    )  


def jbodgen(i: int) -> Jbod:
    return Jbod(
        idx = i,
        wwn0 = ''.join((random.choice(string.hexdigits) for i in range(16))),
        wwn1 = ''.join((random.choice(string.hexdigits) for i in range(16))),
        sasaddr = ''.join((random.choice(string.hexdigits) for i in range(16))),
        mdl = 'JBMD' + ''.join((random.choice(string.digits) for i in range(3))) + ''.join((random.choice(string.ascii_uppercase) for i in range(3))),
        sn = ''.join((random.choice(string.hexdigits) for i in range(8))),
        fw = '.'.join((random.choice(string.octdigits) for i in range(3))),
        state = Jbod.State.ONLINE,
        descr = 'ASCII string of reasonably indeterminate length',
        slots = {str(i): slotgen(i) for i in range(SLOTS_PER_JBOD)}
    )


def plantgen(pid: int) -> Plant:
    return Plant(
        pk = pid,
        testoptions = {1: 'Proper test', 2: 'Solid test', 3: 'Precise test'},
        chosentest = 1, 
        name = 'Relaible drives Inc.', 
        jbods = {str(i): jbodgen(i) for i in range(JBODS_PER_PLANT)}
    )
