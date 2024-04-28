import sys

def remove_duplicates(input_file, output_file):
	existed = []
	wf = open(output_file, 'w')
	with open(input_file, 'r') as f:
		line = f.readline()
		while line:
			if "name=\"Tunnel\"" in line:
				temp_lines = [f.readline() for _ in range(3)]
				temp_lines.insert(0, line)
				long_string = "\n".join(temp_lines)
				if long_string in existed:
					wf.write("\n\n")
				else:
					wf.write(long_string)
					existed.append(long_string)
			else:
				wf.write(line)
			line = f.readline()
	wf.close()


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print(f"Использование: python {sys.argv[0]} <filename>")
		exit()
	# Пример использования
	input_file = sys.argv[1]
	output_file = 'output.circ'
	remove_duplicates(input_file, output_file)

