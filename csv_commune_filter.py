year = 2020

input_file = f'data/FD_LOGEMTZA_{year}.csv'
output_file = f'data/melun/melun_{year}.csv'
code_insee = 77288

with open(input_file, mode='r') as f_in, open(output_file, mode='w') as f_out:
    header = f_in.readline()
    f_out.write(header)

    for line in f_in:
        if line.startswith(str(code_insee)):
            f_out.write(line)
