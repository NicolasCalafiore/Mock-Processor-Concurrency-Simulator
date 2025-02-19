import places
import transitions

# Returns true if all places have exhausted all tokens
def AllComponentsNotExecutable()->bool:
    return not inm.is_executable(1, tick) and not inb.is_executable(1, tick) and not aib.is_executable(1, tick) and not reb.is_executable(1, tick) and not adb.is_executable(1, tick) and not lib.is_executable(1, tick) and not reb.is_executable(1, tick)

# Transfers instructions from IO to lists
def Read_Instructions() -> list[list[str]]:
    instructions = open("instructions.txt", "r").read().split('\n')
    data_memory = open("datamemory.txt", "r").read().split('\n')
    registers = open("registers.txt", "r").read().split('\n')

    return [instructions, data_memory, registers]

def PrintComponents():
    file.write("INM:")
    inm.print(file)
    file.write("INB:")
    inb.print(file)
    file.write("AIB:")
    aib.print(file)
    file.write("LIB:")
    lib.print(file)
    file.write("ADB:")
    adb.print(file)
    file.write("REB:")
    reb.print(file)
    file.write("RGF:")
    rgf.print(file)
    file.write("DAM:")
    dam.print(file)

# Main program cycle. Each call pushes the simulator by one tick. Checks availability of each component to execute a transition
# in a way that mimics concurrency
def Cycle():
    places.Debug.log.append("\n\n New Cycle Started")

    if inm.is_executable(1, tick):
        places.Debug.log.append("\n\n INM EXECUTING DECODE/READ")
        transitions.DECODE(inb, inm, rgf, tick)

    if inb.is_executable(1, tick):
        command = inb.peek()
        keywords = ["<AND", "<SUB", "<ADD", "<OR"]
        if command.split(",")[0] in keywords:
            transitions.ISSUE1(aib, inb, tick)
        else:
            transitions.ISSUE2(lib, inb, tick)

    if lib.is_executable(1, tick):
        transitions.ADDR(adb, lib, tick)

    if adb.is_executable(1, tick):
        transitions.LOAD(reb, dam, adb, tick)

    if aib.is_executable(1, tick):
        transitions.ALU(reb, aib, tick)

    if reb.is_executable(1, tick):
        transitions.WRITE(rgf, reb, tick)


if __name__ == '__main__':
    # Create all places
    dam = places.DAM()
    inb = places.INB()
    rgf = places.RGF()
    inm = places.INM()
    aib = places.AIB()
    reb = places.REB()
    adb = places.ADB()
    lib = places.LIB()

    # Read input and initalize registers with intiial data
    all_instructions = Read_Instructions()

    for i in range(len(all_instructions[2])):
        token = places.TOKEN(all_instructions[2][i])
        rgf.TARGET = i
        rgf.add(token, -2)

    for i in range(len(all_instructions[1])):
        token = places.TOKEN(all_instructions[1][i])
        dam.TARGET = i
        dam.add(token, -2)

    for instruct in all_instructions[0]:
        token = places.TOKEN(instruct)
        inm.add(token, -2)

    tick: int = 0
    with (open("simulation.txt", "w") as file):
        while True:
            file.write(f'STEP {tick}:\n')
            PrintComponents()
            file.write("\n")
            Cycle()
            tick+=1

            if AllComponentsNotExecutable():
                file.write(f'STEP {tick}:\n')
                PrintComponents()
                break

        file.close()

    print("View 'simulation.txt' for results.")
    print("----- DEBUG REPORT -----")
    for log in places.Debug.log:
        print(log)
