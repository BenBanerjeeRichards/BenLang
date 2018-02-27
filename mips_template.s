	.data
		.globl main
        _str_true:		.asciiz "true"
        _str_false:		.asciiz "false"
	.text
	
main: 
{}

	# Quit the program
	li	$v0, 10		# syscall = exit
	syscall

outputInt:
	# Load param
	lw	    $a0, 0($fp)

	# Syscall
	li	$v0, 1	# syscall = print int
	syscall		 
	
	# Delete locals
	move 	$sp, $fp
	lw	$fp, 4($fp)
	
	# Done
	jr	$ra

outputBool:
	# Load param
	lw	$a0, 0($fp)


	beq	$a0, $zero _outputBoolFalse
	li	$v0, 4		# syscall = print_string
	la	$a0, _str_true	# syscall argument
	syscall
	j	_outputBoolDone

	_outputBoolFalse:
	li	$v0, 4		# syscall = print_string
	la	$a0, _str_false	# syscall argument
	syscall

	_outputBoolDone:

	# Delete locals
	move 	$sp, $fp
	lw	$fp, 4($fp)

	# Done
	jr	$ra