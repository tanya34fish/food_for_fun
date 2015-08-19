import glob, sys

if __name__ == '__main__':
    for file in glob.glob(sys.argv[1] + '/*.txt'):
        with open(file, 'r') as f:
            line_arr = []
            for line in f:
                line = line[:len(line) - 1]
                s = raw_input(line)
                if s != '':
                    new_line = s + ' ' + line
                    line_arr.append(new_line)
                else:
                    line_arr.append(line)
            
            f = open(file, 'w')
            for i in line_arr:
                f.write(i + '\n')
            print "\nFile has written"
