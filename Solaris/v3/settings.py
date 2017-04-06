

def get_resolution():
    try:
        file = open('config.txt', 'r')
    except:
        with open('config.txt', 'w') as write_file:
            file_contents = 'resolution 800 600'
            write_file.writelines(file_contents)
        file = open('config.txt', 'r')
    lines = file.readlines()
    file.close()
    for line in lines:
        if line.startswith('resolution'):
            fields = line.split()
            return int(fields[1]), int(fields[2])


def set_resolution(resolution):
    file = open('config.txt', 'r')
    lines = file.readlines()
    file.close()
    for i in range(0, len(lines)):
        line = lines[i]
        if line.startswith('resolution'):
            line = 'resolution ' + str(resolution[0]) + ' ' + str(resolution[1])
            lines[i] = line
            break
    file = open('config.txt', 'w')
    file.writelines(lines)
    file.close()


