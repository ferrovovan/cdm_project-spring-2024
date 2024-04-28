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

