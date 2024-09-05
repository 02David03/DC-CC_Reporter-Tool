#include <stdio.h>
#include <assert.h>
#include "equations.h"

void test_triangle_area() {
    assert(triangle_area(5, 3) == 15);
    assert(triangle_area(7, 2) == 14);
    assert(triangle_area(0, 10) == 0);
}

void test_average_speed() {
    assert(average_speed(100, 20) == 5);
    assert(average_speed(50, 10) == 5);
    assert(average_speed(0, 1) == 0);
}

void test_force() {
    assert(force(10, 9) == 90);
    assert(force(5, 5) == 25);
    assert(force(0, 10) == 0);
}

void test_pythagoras() {
    assert(pythagoras(3, 4) == 25); // 3^2 + 4^2 = 9 + 16 = 25
    assert(pythagoras(6, 8) == 100); // 6^2 + 8^2 = 36 + 64 = 100
    assert(pythagoras(5, 12) == 169); // 5^2 + 12^2 = 25 + 144 = 169
}

int main() {
    test_triangle_area();
    test_average_speed();
    test_force();
    test_pythagoras();

    printf("All test suites passed!\n");
    return 0;
}