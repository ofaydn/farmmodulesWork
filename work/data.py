with open('data.txt') as f:
    line = f.readline()
    while line:
        print(line, end='')
        line = f.readline()
        time.sleep(3)

def count_lines(filename):
    with open(filename, 'r') as f:
        return sum(1 for _ in f)

# Function to get a random line from the file
def get_random_line(filename, num_lines):
    line_number = random.randint(0, num_lines - 1)
    with open(filename, 'r') as f:
        for current_line_number, line in enumerate(f):
            if current_line_number == line_number:
                return line.strip()
            
filename = 'data.txt'
num_lines = count_lines(filename)
random_line = get_random_line(filename, num_lines)