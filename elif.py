if (ratioPeri_Area > 0.025):
	print ("Chili {Mandarin=0, Eggplant=0, Chili=18}")

else (ratioPeri_Area ≤ 0.025):

	if (ratioPeri_Area > 0.023):
		if (ratioPeri_Area > 0.024):
			print("Eggplant {Mandarin=0, Eggplant=2, Chili=0}")
		else (ratioPeri_Area ≤ 0.024):
			print ("Chili {Mandarin=1, Eggplant=0, Chili=4}")
	
	else (ratioPeri_Area ≤ 0.023):
		if (perimeter > 1153.919):
			if (ratioPeri_Area > 0.014):
				if (ratioPeri_Area > 0.021):
					print ("Chili {Mandarin=0, Eggplant=0, Chili=2}")
				else (ratioPeri_Area ≤ 0.021):
					print ("Eggplant {Mandarin=0, Eggplant=29, Chili=0}")
			else (ratioPeri_Area ≤ 0.014):
				print ("Mandarin {Mandarin=3, Eggplant=0, Chili=0}")
		else (perimeter ≤ 1153.919):

			if (perimeter > 899.176):
				if (ratioPeri_Area > 0.020):
					print ("Eggplant {Mandarin=0, Eggplant=6, Chili=0}")
				else (ratioPeri_Area ≤ 0.020):
					if (ratioPeri_Area > 0.019):
						print ("Eggplant {Mandarin=2, Eggplant=4, Chili=0}")
					else (ratioPeri_Area ≤ 0.019):
						print ("Mandarin {Mandarin=17, Eggplant=3, Chili=0}")
			else (perimeter ≤ 899.176):
				print ("Mandarin {Mandarin=22, Eggplant=1, Chili=0}")


