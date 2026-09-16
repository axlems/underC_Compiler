#include <tty.uc>

V0_'dat'() {
    $C8(msg);
}

V0_'main'() {
    (msg) = "hello, World!";
    tty.printv($C8, msg)
}
\\ for easy testing
