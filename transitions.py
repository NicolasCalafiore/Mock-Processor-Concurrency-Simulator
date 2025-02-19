import places

# File contains the actions of all transitions.
# These actions take mostly in the form of transferring one token from one component to the other
# Tokens are then manipulated once it has entered the component.
def DECODE(inb: places.INB, inm: places.INM, rgf: places.RGF, tick):
    inb.add(inm.transfer(),tick, rgf)

def ISSUE2(lib: places.LIB, inb: places.INB,tick):
    lib.add(inb.transfer(),tick)

def ISSUE1(aib: places.AIB, inb: places.INB,tick):
    aib.add(inb.transfer(),tick)

def ALU(reb: places.REB, aib: places.AIB,tick):
    reb.add(aib.transfer(), tick)

def ADDR(adb: places.ADB, lib: places.LIB,tick):
    adb.add(lib.transfer(),tick)

def WRITE(rgf: places.RGF, reb: places.REB,tick, target: int = 0):
    rgf.TARGET = target
    rgf.add(reb.transfer(),tick)

def READ(inb: places.INB, rgf: places.RGF,tick): ## How do i deal with this?
    inb.add(rgf.transfer(),tick)

def LOAD(reb, dam, adb, tick):
    adb_token = adb.transfer()
    parts = adb_token.token_data.strip("<>").split(",")
    dest = parts[0].strip()
    effective_address = int(parts[1].strip())

    data_token = dam.MEM_LIST[effective_address]
    data_parts = data_token.token_data.strip("<>").split(",")
    data_value = data_parts[1].strip()

    new_token_str = f"<LD,{dest},{data_value},0>"
    new_token = places.TOKEN(new_token_str)
    new_token.arrival_tick = tick
    reb.add(new_token, tick)