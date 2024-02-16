surnames = ""
names = ""
middlenames = ""
with open("./wordlists/surnames/surnames_man_and_woman_balanovskya_top10.txt") as surname_file:
	surnames = surname_file.read()
with open("./wordlists/names/first_chars.txt") as name_file:
	names = name_file.read()
with open("./wordlists/middlenames/first_chars.txt") as middlenames_file:
	middlenames = middlenames_file.read()
for surname in surnames.split("\n"):
	for name in names.split("\n"):
		for middlename in middlenames.split("\n"):
			if surname != "" and name != "" and middlename != "":
				print("{0} {1} {2}".format(surname, name, middlename))
