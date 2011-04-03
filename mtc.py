# MTC - Multi-choice Test Checker. 
# This program compares a multi-choice test's answers to its solution, and prints the grade.

from __future__ import with_statement
import sys, os.path

def grade(sol, ans, qnum, pts):
	result = 0
	passes = 0
	for i in range(0, len(ans)):
		if (ans[i] in [" ", "`", ";"] or passes < i + 1 - qnum) and passes < len(ans) - qnum:
			passes += 1
			sys.stdout.write(str(passes))		# passed this question; indicate this
		elif (ans[i] in sol[i]):
			result += pts
			sys.stdout.write(" ")
		else:
			sys.stdout.write("!")
	print
	return result

def get_number():
	tmp = raw_input()
	if not tmp.isdigit():
		print "Error: must be a number."
		tmp = None
	else:
		tmp = int(tmp)
		if tmp < 0:
			print "Error: must be a non-negative number."
			tmp = None
	return tmp

def show_menu(d):
	print
	print "Welcme to the multi-choice test checker. What would you like to do?"
	print "1 - save a new solution."
	print "2 - check a test."
	print "3 - set the number of questions to be chosen in a test ( current:", str(d.qnum), ")."
	print "4 - set the amount of points per question ( current:", str(d.pts), ")."
	print "5 - view the saved solutions"
	print "6 - get help on this program."
	print "7 - exit."

def get_solution(d):
	print "Which version, 1 or 2?"
	ver = get_number()
	if not ver in [1,2]:
		print "Allowed versions are only 1 and 2."
		return
	ver -= 1		# make it [0,1] to match the indices
	d.sols[ver] = []
	print "Please enter the solution (enter an empty line to indicate the end of the solution):"
	i = 1
	while True:
		sys.stdout.write(str(i))
		print ". ",
		anstr = raw_input()
		if anstr == "": break
		i += 1
		curans = []
		for c in anstr:
			curans.append(c)
		d.sols[ver].append(curans)
	print "This version has", i - 1, "questions."	

def check_answers(d):
	cont = ""
	while cont == "":
		if d.sols[0] != [] and d.sols[1] != []:
			print "Which version, 1 or 2?"
			ver = get_number()
			if not ver in [1,2]:
				print "Allowed versions are only 1 and 2."
				break
		elif d.sols[0] != []:
			ver = 1
		elif d.sols[1] != []:
			ver = 2
		else:
			print "Please save a solution first."
			break
		print "The test version is", ver, "."
		ver -= 1		# make it [0,1] to match the indices
		print "Please enter the answers:"
		ans = raw_input()
		if ans == "": break
		if len(ans) != len(d.sols[ver]):
			print "Error: answer sheet length does not match solution."
			break
		result = grade(d.sols[ver], ans, d.qnum, d.pts)
		print "The grade is:", result		# first evaluate, so the printing turns out well
		print "Press Enter to check another test, or type anything and press Enter to finish..."
		cont = raw_input()

def get_qnum(d):
	print "Please enter the number of questions to be chosen in a test ( current:", str(d.qnum), "):",
	tmp = get_number()
	if tmp != None: d.qnum = tmp

def get_pts(d):
	print "Please enter the amount of points per question ( current:", str(d.pts), ").",
	tmp = get_number()
	if tmp != None: d.pts = tmp

def review_sol(d):
	i = 0
	for sol in d.sols:
		i += 1
		if sol == []: continue
		print "Version", str(i), ":"
		j = 0
		for q in sol:
			j += 1
			print str(j), ":",
			for a in q:
				print a,
			print

def show_help():
	print
	print "Save a solution, and then type in the answers to check them."
	print "To enter a solution, for each question, type a string of its possible answers,"
	print "and press enter. To indicate there are no more questions,"
	print "type nothing and press enter."
	print "An answer-sheet is a string of characters,"
	print "each representing an answer to a single question."
	print "An answer can be any single character."
	print "A space, ` or ; will be considered a pass on the question."
	print "After getting the grade, type anything and press Enter"
	print "to return to the menu, or just press Enter to check another test."

class data():
	def __init__(self, qnum, pts):
		self.sols = [[], []]
		self.qnum = qnum
		self.pts = pts

def load_data(filename, d):
	if os.path.isfile(filename):
		with open(filename, "r") as FILE:
			d.qnum = int(FILE.readline().rstrip("\n"))
			d.pts = int(FILE.readline().rstrip("\n"))
			FILE.readline()		# line's space between parameters and solutions
			for sol in d.sols:
				while True:
					line = FILE.readline()
					if line == "": return
					line = line.rstrip("\n")
					if line == "": break
					ans = []
					for c in line:
						ans.append(c)
					sol.append(ans)

def save_data(filename, d):
	with open(filename, "w") as FILE:
		FILE.write(str(d.qnum) + "\n")
		FILE.write(str(d.pts) + "\n")	
		for sol in d.sols:
			FILE.write("\n")		# line's space between parameters and solutions
			for ans in sol:
				for c in ans:
					FILE.write(c)
				FILE.write("\n")
			
OPT_SOLUTION = 1 ; OPT_ANSWERS = 2 ; OPT_NUM = 3
OPT_PTS = 4 ; OPT_REV = 5 ; OPT_HELP = 6 ; OPT_EXIT = 7
opt = 0

d = data(20, 5)	# 20 questions, 5 points each
load_data("settings.mtcdata", d)

while True:
	show_menu(d)
	opt = get_number()
	if opt == OPT_SOLUTION: get_solution(d)
	elif opt == OPT_ANSWERS: check_answers(d)
	elif opt == OPT_NUM: get_qnum(d)
	elif opt == OPT_PTS: get_pts(d)
	elif opt == OPT_REV: review_sol(d)
	elif opt == OPT_HELP: show_help()
	elif opt == OPT_EXIT: exit()
	save_data("settings.mtcdata", d)
	print
	print "Press Enter to return to the menu..."
	raw_input()
