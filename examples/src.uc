#include <tty>
#include <sys>

V0_'data'(){
	I64(x);
	I64(y);	
}

V0_'main'(){
	// this is a register interaction
	R64(rax) = 10;
        (x) = (rax);
	(rax) = xor (rax), (rax);
        (y) = adition(x, 1);
        tty_puts("10 + 1");
	if (y == 11) {
        tty_printf(" = %d", y);
	}
	elif (y > 9) {
	asm[";hello assembly"];
	(y)= add (y), (y);
	}
	else {
        sys.exit();
	}
}


I64_'addition'(I64_'a', I64_'b'){
	return(a + b);
}
