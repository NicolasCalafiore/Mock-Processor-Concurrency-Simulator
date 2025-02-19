# Used for debug report after run
class Debug:
    log: list[str] = []

# Container to hold memory data
class TOKEN:
    def __init__(self, token_data:str):
        self.token_data = token_data
        self.arrival_tick = -1

# Interface for all places
class PLACE:
    def __init__(self):
        self.data = []
        self.max_tokens = 100

    def token_count(self)->int:
        return len(self.data)

    def print(self, file) -> None:
        tokens = [token.token_data.replace(" ", "").replace("\t", "") for token in self.data]
        file.write(",".join(tokens) + "\n")

    def is_executable(self, cost, curr_tick)->bool:
        Debug.log.append(f'Is {self.__class__.__name__} executable?')
        if len(self.data) == 0:
            Debug.log.append(f'Empty {self.__class__.__name__}')
            return False
        else:
            Debug.log.append(f'Arrival Tick: {self.data[0].arrival_tick} vs Current Tick: {curr_tick}')
            Debug.log.append(str(self.data[0].arrival_tick < curr_tick))
        return len(self.data) >= cost and self.data[0].arrival_tick < curr_tick

    def transfer(self):
        Debug.log.append(f'Token {self.data[0].token_data} transferred from {self.__class__.__name__}')
        if len(self.data) == 0:
            return "ERROR"
        temp = self.data[0]
        self.data.pop(0)
        return temp

    def peek(self) -> str:
        return self.data[0].token_data

    def add(self, token: TOKEN, tick):
        Debug.log.append(f'Token {token.token_data} added to {self.__class__.__name__}')
        token.arrival_tick = tick
        self.data.append(token)


class DAM(PLACE):
    TARGET: int = 0  # To be manipulated/accessed from Psim.py

    def __init__(self):
        super().__init__()
        self.MEM_LIST: list[None | TOKEN] = []
        self.MEM_LIST.append(None) # Should always be None? R0 != Exist?
        self.MEM_LIST.append(None)
        self.MEM_LIST.append(None)
        self.MEM_LIST.append(None)
        self.MEM_LIST.append(None)
        self.MEM_LIST.append(None)
        self.MEM_LIST.append(None)
        self.MEM_LIST.append(None)
        self.MEM_LIST.append(None)


    def add(self, token: TOKEN, tick):
        Debug.log.append(f'Token {token.token_data} added to {self.__class__.__name__}')
        token.arrival_tick = tick
        self.MEM_LIST[self.TARGET] = token


    def peek(self):
        return self.MEM_LIST[self.TARGET].token_data

    def print(self, file):
        tokens = [memory.token_data for memory in self.MEM_LIST if memory is not None]
        message = ",".join(tokens)
        file.write(message[0:-1]  + "\n")   # For some reason there's a trailing comma


class RGF(PLACE):
    def __init__(self):
        super().__init__()
        self.MEM_LIST: list[None | TOKEN] = [None] * 8



    def add(self, token: TOKEN, tick):
        Debug.log.append(f'Token {token.token_data} added to {self.__class__.__name__}')
        token.arrival_tick = tick
        parts = token.token_data.strip("<>").split(",")
        reg_name = parts[0]
        index = int(reg_name.replace("R", ""))
        self.MEM_LIST[index] = token

    def peek(self):
        return self.MEM_LIST[0].token_data if self.MEM_LIST[0] is not None else "None"

    def get_register_value(self, reg_name: str) -> str | None:
        index = int(reg_name.replace("R", ""))
        token = self.MEM_LIST[index]
        if token is not None:
            parts = token.token_data.strip("<>").split(",")
            return parts[1]
        return None

    def print(self, file):
        tokens = [
            memory.token_data.replace(" ", "").replace("\t", "")
            for memory in self.MEM_LIST
            if memory is not None
        ]
        file.write(",".join(tokens) + "\n")


class INM(PLACE):   # Holds all instructions
    def __init__(self):
        super().__init__()



class INB(PLACE):
    def __init__(self):
        super().__init__()

    def add(self, token: TOKEN, tick, rgf: 'RGF' = None):
        if rgf is not None:

            parts = token.token_data.strip("<>").split(",")
            if len(parts) == 4:
                opcode, dest, src1, src2 = parts

                val1 = rgf.get_register_value(src1)
                val2 = rgf.get_register_value(src2)

                token = TOKEN(f"<{opcode},{dest},{val1},{val2}>")
        token.arrival_tick = tick
        self.data.append(token)





class LIB(PLACE):
    def __init__(self):
        super().__init__()


class ADB(PLACE):
    def __init__(self):
        super().__init__()

    def add(self, token: TOKEN, tick):
        command = token.token_data.split(",")
        output = f'<{command[1]}, {(int(command[2])) + int((command[3]).replace(">", ""))}>'
        new_token = TOKEN(output)
        new_token.arrival_tick = tick
        self.data.append(new_token)



class REB(PLACE):
    def __init__(self):
        super().__init__()

    def add(self, token: TOKEN, tick):
        command = token.token_data.split(",")
        #<R4,3>
        opcode = command[0]
        dest = command[1]
        val1 = int(command[2])
        val2 = int(command[3].replace(">", ""))

        if opcode == "<ADD":
            result = val1 + val2
        elif opcode == "<SUB":
            result = val1 - val2
        elif opcode == "<AND":
            result = val1 & val2
        elif opcode == "<OR":
            result = val1 | val2
        elif opcode == "<LD":
            result = val1
        else:
            result = "ERROR"

        new_token = TOKEN(f'<{dest}, {result}>')
        new_token.arrival_tick = tick
        self.data.append(new_token)


class AIB(PLACE):
    def __init__(self):
        super().__init__()
