from change_circ_functions import *


# TODO
def wire_delta():
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


# TODO
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



def add_many_registers(main_circuit,
	start_coords: (int, int), delta: (int, int), rows: int, columns: int,
	register_font='Sawasdee plain 12'):
	base_x = start_coords[0]
	base_y = start_coords[1]


	tag = 'comp'

	attrib = {'lib': '4',
		'loc': f'({base_x},{base_y})',
		'name': 'Register'
	}
	sub_elements = {
		'width': '32',
		'trigger': 'falling',
		'label': 'reg',
		'labelfont': register_font
	}
	register = Element(tag, attrib, sub_elements)


	attrib = {'lib': '0', 'name': 'Pin',
		'loc': f'({base_x},{base_y})'
	}
	sub_elements = {
		'facing': 'west',
		'width': '32',
		'output': 'true',
		'tristate': 'false',

		'labelloc': 'north',
		'label': 'out_reg',
		'labelfont': "Sawasdee plain 12",
	}
	pin_out = Element('comp', attrib, sub_elements)

	attrib = {'lib': '0', 'name': 'Tunnel',
		'loc': f'({base_x - 30},{base_y})'
	}
	sub_elements = {
		'width': '32',
		'facing': 'east',
		'label': 'to_reg',
	}
	tunnel_to = Element(tag, attrib, sub_elements)

	attrib['loc'] = f'({base_x - 20},{base_y+20})'
	sub_elements['label'] = 'active_reg'
	sub_elements['facing'] = 'north'
	sub_elements['width'] = '1'
	tunnel_active = Element(tag, attrib, sub_elements)
	
	parent_elems = [register,
		pin_out,
		tunnel_to,
		tunnel_active
	]
	
	mult_elems(main_circuit, parent_elems,
		delta, rows, columns)

	
#TODO:
#diagonal_elems(main_circuit, active_tunnels_banch(),
#	(10, 30),
#	4, 8)

