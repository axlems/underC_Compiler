#include <tty>
#include <sys>

V0_'data'(){
    I64(x);
    I64(y);

    @I64(numbers);
    @I8(message);

    *I64(ptr);
    *@I64(arrayPtr);
    @*I64(ptrArray);

    B1(flag);
}

V0_'main'(){
    // Basic variables
    (x) = 10;
    (y) = 20;

    // Register interaction
    RI64(rax) = 10;
    (x) = (rax);

    (rax) += 5;
    (y) = (rax);

    (rax) ^= (rax);

    // Array
    @I64(numbers) = {10, 20, 30, 40, 50};

    (numbers[0]) = 100;
    (numbers[1]) += 5;

    // Pointer
    *I64(ptr) = &(x);

    (y) = *(ptr);

    // Pointer to an array
    *@I64(arrayPtr) = &(numbers);

    (y) = *(arrayPtr[0]);

    // Array of pointers
    @*I64(ptrArray);

    (ptrArray[0]) = &(x);
    (ptrArray[1]) = &(y);

    (x) = *(ptrArray[0]);
    (y) = *(ptrArray[1]);

    // Character array acting as a string
    @I8(message) = "Hello, _C!";

    tty.puts(message);

    // Boolean
    (flag) = true;

    if (flag) {
        tty.puts("Boolean is true");
    }
    elif (x > 10) {
        tty.puts("x is greater than 10");
    }
    else {
        tty.puts("Nothing happened");
    }

    // Arithmetic
    (x) = (x) + (y);
    (x) -= 5;
    (x) *= 2;
    (x) /= 5;

    // Comparison
    if (x == y) {
        tty.puts("x == y");
    }
    elif (x != y) {
        tty.puts("x != y");
    }

    if (x >= 10 && y <= 20) {
        tty.puts("comparison passed");
    }

    // Boolean operations
    (flag) = (flag) && true;
    (flag) = (flag) || false;
    (flag) = !(flag);

    // Bitwise operations
    (x) = (x) & (y);
    (x) = (x) | (y);
    (x) = (x) ^ (y);

    // Increment / decrement
    (x)++;
    (y)--;

    // Compound shifts
    (x) <<= 1;
    (y) >>= 1;

    // Inline assembly
    asm["mov rax, 1"];

    // Function call
    (y) = addition(x, 1);

    tty.printf("Result: %d", y);

    sys.exit();
}

I64_'addition'(I64_'a', I64_'b'){
    return(a + b);
}
