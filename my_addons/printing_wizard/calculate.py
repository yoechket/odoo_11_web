#!/usr/bin/python
# -*- coding: utf-8 -*-
def calculate_format(inh, inw, outh, outw):
	# https: // quire.io / w / Provendo_Thuretrykk / 14 / Legge_inn_marger_i_f...?group = priority
#	inh = inh - 25
#	outh += 3
#	outw += 3
#
#	inm2 = inh * inw
#	outm2 = (outh + 0.3) * (outw + 0.3)
#
#	antp = int((inh - 0.3) / (outh + 0.3))*int((inw - 0.3) / (outw + 0.3))
#	antl = int((inh - 0.3) / (outw + 0.3))*int((inw - 0.3) / (outh + 0.3))
#	if (antp <= antl) : ant = antl ; direction = "landscape"
#	if (antl < antp) : ant = antp ; direction = "portrait"
#	svinn = (inm2 - (outm2 * ant))/10000

	inh = inh - 28
	inw = inw - 3
	outh += 3
	outw += 3
	inm2 = inh * inw
	outm2 = (outh) * (outw)

	antp = int((inw/outh)*(inh/outw))
	antl = int((inw/outw)*(inh/outh))
	if (antp <= antl) : ant = antl ; direction = "landscape"
	if (antl < antp) : ant = antp ; direction = "portrait"
	svinn = (inm2 - (outm2 * ant))/100

	return ant, direction, svinn

if __name__ == '__main__':
	inh = 60
	inw = 120
 
	outh = 25
	outw = 10

	ant, direction, svinn = calculate_format(inh, inw, outh, outw)
	print("Du får %d eksemplarer og %.2f cm2 i svinn hvis du velger %s format." % (ant, svinn, direction))
	#print "Du får %d eksemplarer og %.2f m2 i svinn hvis du velger %s format." % (ant, (inm2 - (outm2 * ant))/10000, direction)
 
""" 
inh og inw er høyde og bredde på rå formatet (arket som skal inn i maskinen).
outh og outw er høyde og bredde på slutt produktet (arket som kunden har bestilt).
 
Formelen gir oss hvilken vei det bør trykkes, hvor mange man få plass til på rå formatet samt at man får vite hvor mye av rå formatet man ikke får brukt.
Svinn bruker vi til å finne hvilket rå format som er best.
"""

