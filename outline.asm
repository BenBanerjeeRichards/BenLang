	.data
		.globl main
	.text
	
main: 
	# Quit the program
	li	$v0, 10		# syscall = exit
	syscall

# Output an integer
# PARAMS:
# 	$a0	The ingeger to print
# RETURN: NONE

outputInt:
	li	$v0, 1	# syscall = print int
	syscall		# $a0 already contains integer 
	jr	$ra