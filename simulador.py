# vetor memória
memory = []
# quantidade de endereços da memória
memory_size = 64
# banco de registrador = 8
regs = [0, 0, 0, 0, 0, 0, 0, 0]

cpu_alive = True

cycle = 0

# guardar endereco da próxima instrução
reg_pc = 0
# registrador guardar a instrução lida na memória
reg_inst = 0

# decodificando instruções
decoded_inst = {
    'type'  : 0,
    'opcode': 0,

    'r_dest': 0,
    'r_op1' : 0,
    'r_op2' : 0,

    'i_reg' : 0,
    'i_imed': 0,
}

def error(error):
    print('ERROR: {}' .format(error))

def extract_bits (num, bit_init, bit_len):
    # num: posicao reg_inst
    # bit_init: em qual bit começa a instrução
    # bit_len: tamanho de bits que a instrução possui
    num = num >> bit_init
    mask = (1 << bit_len) - 1
    return num & mask

def fetch():
    global reg_pc, reg_inst
    print('Fetch addr {}' .format(reg_pc))
    # setando em reg_inst o endereco de instrução que será executada nesse ciclo
    reg_inst = memory[reg_pc]
    # setando o endereco da próxima instrução
    reg_pc = reg_pc + 1

def decode():
    global reg_inst, decoded_inst

    print('Decode inst {}' .format(reg_inst))

    # seta no atributo type o bit 15 para saber se a instrução é do tipo i ou r
    decoded_inst['type'] = extract_bits(reg_inst, 15, 1)

    # se for r
    if decoded_inst['type'] == 0:
        decoded_inst['opcode'] = extract_bits(reg_inst, 9, 6)
        decoded_inst['r_dest'] = extract_bits(reg_inst, 6, 3)
        decoded_inst['r_op1'] = extract_bits(reg_inst, 3, 3)
        decoded_inst['r_op2'] = extract_bits(reg_inst, 0, 3)
    
    elif decoded_inst['type'] == 1:
        decoded_inst['opcode'] = extract_bits(reg_inst, 13, 2)
        decoded_inst['i_reg'] = extract_bits(reg_inst, 10, 3)
        decoded_inst['i_imed'] = extract_bits(reg_inst, 0, 9)
    
    else:
        error('bit 15 do not have a valid type')

def execute():
    global decoded_inst, reg_pc, cpu_alive, regs, memory, memory_size

    print('excute inst')
    print(decoded_inst)

    # operação r
    if decoded_inst['type'] == 0:
        opcode = decoded_inst['opcode']
        r_dest = decoded_inst['r_dest']
        r_op1 = decoded_inst['r_op1']
        r_op2 = decoded_inst['r_op2']
        # add (soma)
        if opcode == 0:    
            print('add r{}, r{}, r{}' .format(r_dest, r_op1, r_op2))
            regs[r_dest] = regs[r_op1] + regs[r_op2]

        # sub 
        elif opcode == 1:
            print('sub r{}, r{}, r{}' .format(r_dest, r_op1, r_op2))
            regs[r_dest] = regs[r_op1] - regs[r_op2]

        # mul 
        elif opcode == 2:
            print('mul r{}, r{}, r{}' .format(r_dest, r_op1, r_op2))
            regs[r_dest] = regs[r_op1] * regs[r_op2]

        # div
        elif opcode == 3:
            print('div r{}, r{}, r{}' .format(r_dest, r_op1, r_op2))
            regs[r_dest] = regs[r_op1] / regs[r_op2]
    elif decoded_inst['type'] == 1:
        opcode = decoded_inst['opcode']
        i_imed = decoded_inst['i_imed']
        i_reg = decoded_inst['i_reg']

        # jump
        if opcode == 0:
            print('jump {}' .format(i_imed))
            reg_pc = i_imed

        else:
            print('opcode {}' .format(opcode))
            cpu_alive = False

        print(regs)



def cpu_loop():
    global cycle

    print('------------------------------')
    print('cycle {}' .format(cycle))

    fetch()
    decode()
    execute()

    cycle = cycle + 1

def main():
    global memory, memory_size, cpu_alive, regs

    # preenchendo os endereços da memória
    for i in range(0, memory_size):
        memory.append(0x0000)
    print('Memory size (words): {}' .format(len(memory)))

    z = 0

    memory[z] = 0b1110000000000001  # mov r0, 1
    z = z + 1
    memory[z] = 0b1110100000001000  # mov r2, 8
    z = z + 1
    memory[z] = 0b1110010000000001  # mov r1, 1
    z = z + 1
    memory[z] = 0b1111000000010100  # mov r4, 20
    z = z + 1
    memory[z] = 0b0000010101001001  # mul r5, r1, r1
    z = z + 1
    memory[z] = 0b0010000000100101  # store [r4], r5
    z = z + 1
    memory[z] = 0b0000000100100000  # add r4, r4, r0
    z = z + 1
    memory[z] = 0b0000000001001000  # add r1, r1, r0
    z = z + 1
    memory[z] = 0b0000101011001010  # cmp_neq r3, r1, r2
    z = z + 1
    memory[z] = 0b1010110000000100  # jump_cond r3, 4
    z = z + 1
    memory[z] = 0b0111111000000000  # halt inst
    z = z + 1
	
	# executando o processo enquanto cpu = alive
    while cpu_alive:
        cpu_loop()

    print(regs)
    print(memory)

    print('pysim halted')

main()