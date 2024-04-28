import sys
import xml.etree.ElementTree as ET


class Element:
	def __init__(self, tag: str, attrib: dict, sub_elements: dict):
		self.tag = tag
		self.attrib = attrib.copy()
		self.sub_elements = sub_elements.copy()

	def get_coords(self, attr_name) -> list:
		str_coords = self.attrib[attr_name].strip('()').split(',')
		return [int(coord) for coord in str_coords]

	def moved_coords(self, attr_name, delta_coords: (int, int)) -> tuple:
		coords = self.get_coords(attr_name)
		return (coords[0] + delta_coords[0], coords[1] + delta_coords[1])

	def build(self, delta_coords: (int, int) , new_name: str):
		new_coords = self.moved_coords('loc', delta_coords)

		new_attrib = self.attrib.copy()
		new_attrib['loc'] = str(new_coords)

		new_element = ET.Element(self.tag, new_attrib)
		
		new_sub_elements = self.sub_elements.copy()
		new_sub_elements['label'] = new_name

		# Создание подэлементов для элемента
		for key, val in new_sub_elements.items():
			sub_element = ET.SubElement(new_element, 'a', {'name': key, 'val': val})
		return new_element


def mult_elems(main_circuit, parents,
		delta_coords: (int, int),
		rows: int, columns: int
	):

	def add_elem(parent, elem_num):
		prefix = parent.sub_elements['label']
		xml_element = parent.build(
			(delta_coords[0] * column,
			delta_coords[1] * row),
			f"{prefix}{elem_num}"
		)
		main_circuit.append(ET.Comment('\n\n'))
		main_circuit.append(xml_element)
		main_circuit.append(ET.Comment('\n\n'))

	
	for row in range(rows):
		for column in range(columns):
			elem_num = column * rows + row + 1

			for parent in parents:
				add_elem(parent, elem_num)


def diagonal_elems(main_circuit, parent: Element,
		delta_coords: (int, int),
		rows: int, columns: int
	):

	main_circuit.append(ET.Comment('\n\n'))
	for column in range(columns):
		for row in range(rows):
			elem_num = column * max_row + row + 1
			cur_delta_x = delta_coords[0] * (column * max_row + row)
			cur_delta_y = delta_coords[1] * row

			xml_element = parent.build(
				(cur_delta_x, cur_delta_y),
				f"active_reg{elem_num}"
			)
			main_circuit.append(xml_element)
			main_circuit.append(ET.Comment('\n'))


			
def wire_delta():
	# TODO
	start_coords = base_wire.moved_coords("from",
		(cur_delta_x, delta_y * row)
	)
	
	end_coords = base_wire.get_coords("to")
	end_coords = (end_coords[0] + cur_delta_x, end_coords[1])
	
	new_attrib = base_wire.attrib.copy()
	new_attrib['from'] = str(start_coords)
	new_attrib['to'] = str(end_coords)

	new_element = ET.Element(base_wire.tag, new_attrib)
	main_circuit.append(xml_element)
	main_circuit.append(ET.Comment('\n'))


def active_tunnels_banch() -> [Element]:
	base_x = 90
	base_y = 510

	tag = 'comp'
	attrib = {'lib': '0', 'name': 'Tunnel',
		'loc': f'({base_x},{base_y})'
	}
	sub_elements = {
		'width': '1',
		'facing': 'south',
		'label': 'active_reg',
	}
	tunnel_active = Element(tag, attrib, sub_elements)
	
	attrib = {'from': str((base_x, base_y)), 'to': str((base_x, 740))}
	base_wire = Element("wire", attrib, {})


def registers_banch() -> [Element]:
	base_x = 120
	base_y = 80

	tag = 'comp'
	attrib = {'lib': '4',
		'loc': f'({base_x},{base_y})',
		'name': 'Register'
	}
	sub_elements = {
		'width': '32',
		'trigger': 'falling',
		'label': 'reg',
		'labelfont': 'Sawasdee plain 12'
	}
	register = Element(tag, attrib, sub_elements)


	attrib = {'lib': '0', 'name': 'Tunnel',
		'loc': f'({base_x},{base_y})'
	}
	sub_elements = {
		'width': '32',
		'facing': 'west',
		'label': 'from_reg',
	}
	tunnel_from = Element(tag, attrib, sub_elements)

	attrib['loc'] = f'({base_x - 30},{base_y})'
	sub_elements['label'] = 'to_reg'
	sub_elements['facing'] = 'east'
	tunnel_to = Element(tag, attrib, sub_elements)

	attrib['loc'] = f'({base_x - 20},{base_y+20})'
	sub_elements['label'] = 'active_reg'
	sub_elements['facing'] = 'north'
	sub_elements['width'] = '1'
	tunnel_active = Element(tag, attrib, sub_elements)
	
	parent_elems = [register,
		tunnel_from,
		tunnel_to,
		tunnel_active
	]
	return parent_elems


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


	#mult_elems(main_circuit, registers_banch(),
	#	(180, 100), 8, 4)

	#diagonal_elems(main_circuit, active_tunnels_banch(),
	#	(10, 30),
	#	4, 8)


	tag = 'comp'
	attrib = {'lib': '0', 'name': 'Tunnel',
		'loc': '(1600,400)'
	}
	sub_elements = {
		'width': '32',
		'facing': 'west', #'north',
		'label': 'to_reg',
	}
	tunnel_to = Element(tag, attrib, sub_elements)
	mult_elems(main_circuit, [tunnel_to],
		(0, 10), 32, 1)
	#mult_elems(main_circuit, [tunnel_to],
	#	(10, 0), 1, 32)

	tree.write(f"mod_{filename}", encoding='utf-8',
		xml_declaration=True
	)

