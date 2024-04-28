from change_circ_functions import *
from change_circ_examples import add_many_registers
			


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print(f"Использование: python {sys.argv[0]} <filename>")
		exit()

	filename = sys.argv[1]
	if not filename.endswith('.circ'):
		print("Неверное расширение файла. Пожалуйста, укажите файл с расширением '.circ'")
		exit()

	tree = ET.parse(filename)
	root = tree.getroot()
	# Нахождение элемента <circuit> с атрибутом name="main"
	main_circuit = root.find(".//circuit[@name='main']")


	add_many_registers(main_circuit, (1700, 80), (200, 140), 4, 8 )
	"""
	attrib = {'lib': '0', 'name': 'Tunnel',
		'loc': '(1600,400)'
	}
	sub_elements = {
		'width': '32',
		'facing': 'west', #'north',
		'label': 'to_reg',
	}
	tunnel_to = Element('comp', attrib, sub_elements)
	
	#straight_elem(main_circuit, tunnel_to, vect="horizontally", vect_len=10)
	#straight_elem(main_circuit, tunnel_to, vect="vertically", vect_len=10)
	"""

	tree.write(f"mod_{filename}", encoding='utf-8',
		xml_declaration=True
	)

