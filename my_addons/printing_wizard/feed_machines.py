#!/usr/bin/env python3

import odoorpc


ENV = 'txt'

if ENV == 'dev':
	o = odoorpc.ODOO('localhost')
	o.login('o10thure', 'torvald@bringsvor.com', 'Test123')
else:
	o = odoorpc.ODOO('localhost')
	o.login('o10thuretrykk', 'terje@provendo.no', 'Test123')

prod_o = o.env['product.product']

machines = {}

machines['trykk'] = [
('Roland 700 4 farger + lakk', 72, 102),
('Heidelberg vinge A4+', 25, 35),
('Heidelberg vinge hot foil', 25, 35),
('Kodak platesetter', 72, 102),
]

machines['ferdiggjoring'] = [
('MBO 76 falsemaskin', 72, 102),
('MBO 52 falsemaskin', 52, 72),
('Wolenberg', 115, None),
('Duplo', 32, 45),
('Zund skjær og fresebord', 320, None),
('Stitchliner samlestifter', 23, 34),
('Stago sadelstifter', 22.5, 50),
('Polygraph sadelstifter', 32, 50),
('Stitchliner limfres', 32, 32),
('Stitchliner stansemaskin', 40, 55),
('Stitchliner rill og perforerings',36, 85),
('Hang hullemaskin - alle format 4 hull', None, None),
('Foliant Mercury', 52, 72)
]

machines['digital_ark'] = [
('Xerox Igen', 36.4, 66),
('Xerox Igen', 36.4, 66),
('Xerox 550', 32, 45),
('Xerox 4110', 32, 45),
('MGI punktlakk og hotfoil', 36, 102),
]

machines['digital_rull'] = [
('Canon IPF 9000', 160, None),
('Canon IPF 9400S', 160, None),
('Colorwave 700', 106, None),
('HP Latex', 160, None),
('Seikon Colorpainter', 260, None),
('Arizona', 250, 305),
]

# Kostnader
cost = {
'Roland 700 4 farger + lakk': # - 72x102 max format
(2800.00, 0.25),
'Heidelberg vinge A4+': # - 25x35 max format
(650.00, 0.25),
'Heidelberg vinge hot foil': # – 25x35 max format
(1500.00, 0.35),
'Kodak platesetter': # - 72x102 max format
(0.00, 250.00),

#FERDIGGJØRING:
'MBO 76 falsemaskin': # – 15x25 min. Format /72x102 max format
(650.00, 0.05),
'MBO 52 falsemaskin': # - 15x15min. Format /52x72 max format
(450.00, 0.05),
'Wolenberg': # – 115 max format
(350.00, 0.05),
'Duplo': #– 36x66 max format
(450.00, 1),
'Zund skjær og fresebord': #320x250 max format
(450.00, 25.0),
'Stitchliner samlestifter': # min. Format 8,5x12 / max format 23x34
(1000.00, 0.65),
'Stago sadelstifter': #22,5x50 max format
(250.00, 3.50),
'Polygraph sadelstifter': #- 32x50 max format
(250.00, 3.50),
'Stitchliner limfres': #– min format 10,5x13,5 / max format 32x32
(650.00, 10.0),
'Stitchliner stansemaskin': #– min format 20x27,5 / max format 40x55
(1200.00, 0.25),
'Stitchliner rill og perforerings': #- min format 10,5x18 / max format 36x85
(450.00, 1),
'Hang hullemaskin - alle format 4 hull': #- min format 21x29,7
(450.00, 0.10),
'Foliant Mercury': #- max format 52x72
(450.00, 4.5),
#DIGITALTRYKK ARK:
'Xerox Igen': # - 36,4x66 max format
(450.00, 7.00),
'Xerox Igen': # - 36,4x66 max format
(450.00, 7.00),
'Xerox 550': # - 32x45 max format
(450.00, 7.00),
'Xerox 4110': # - 32x45 max format
(450.00, 1.50),
'MGI punktlakk og hotfoil': # – 36x102 max format
	(2500.00, 1100.00),
# DIGITALTRYKK RULL:
'Canon IPF 9000': # – 160 max bredde
(450.00, 1.00),
#Pr m2       kr avhengig av materiale

'Canon IPF 9400S': #– 160 max bredde
(450.00, 1.00),
#Pr m2       kr avhengig av materiale

'Colorwave 700':# – 106 max bredde
(450.00, 1.00),
#Pr m2       kr avhengig av materiale

'HP Latex': # – 160 max bredde
(450.00, 1.00),
#Pr m2       kr avhengig av materiale

'Seikon Colorpainter': # – 260 max bredde
(450.00, 1.00),
#Pr m2       kr avhengig av materiale

'Arizona': # – 250x305 max formatH
(450.00, 1.00),
#Pr m2       kr avhengig av materiale
}

def check_products(machine, costinfo):
	print('CHECK_PRODUCTS', machine.name, costinfo)
	print('WHAT IT IS', machine.startup_product, machine.running_product)
	if not machine.startup_product:
		running_name = 'Oppstart ' + machine.name
		prod = prod_o.browse(prod_o.search([('name', '=', running_name)]))
		print('PROD', prod, bool(prod))
		if not prod:
			info = {'name': running_name,
					'list_price': costinfo[0]}
			idd = prod_o.create(info)
			machine.startup_product = prod_o.browse(idd)
			print('CREATED', idd, machine.startup_product)

	if not machine.running_product:
		running_name = 'Forbruk ' + machine.name
		prod = prod_o.browse(prod_o.search([('name', '=', running_name)]))
		print('PROD', prod, bool(prod))
		if not prod:
			info = {'name': running_name,
					'list_price': costinfo[1]}
			idd = prod_o.create(info)
			machine.running_product = prod_o.browse(idd)
			print('CREATED', idd, machine.running_product)

mach = o.env['printing_wizard.machine']

for mtype, spec in machines.items():
	print('MTY', mtype)
	for minfo in spec:
		print('MINFO', minfo)
		name, width, height = minfo
		mid = mach.browse(mach.search([('name', '=', name)]))
		if mid:
			print('EXISTS', mid)
			same = mid.name == name and (height and mid.max_height == height or True) and (width and mid.max_width == width or True) and mid.maskintype == mtype
			print('SAME?', same, mid.name == name, mid.max_height == height, mid.max_width == width, mid.maskintype == mtype)
			c = cost[name]
			print('C', c)
			check_products(mid, c)
		else:
			info = {'name': name,
				'maskintype': mtype,
				'max_height': height,
				'max_width': width
			}

			idd = mach.create(info)
			print('Created', idd)

form = o.env['printing_wizard.output_format']

formats = [
	('A4', 21.0, 29.7),
	('A3', 29.7, 42.0),
	('A2', 42.0, 59.4),
	('A1', 59.4, 84.1),
	('A0', 84.1, 118.9),
]


for name, width, height in formats:
	exists = form.search([('name', '=', name)])
	if exists:
		print('FINST', name)
		continue

	info = {'name': name,
		'width': width,
		'height': height
		}
	form.create(info)
