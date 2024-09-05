#include <stdio.h>
#include "equations.h"

// Arithmetic functions
int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

int divide(int a, int b) {
    if (b == 0) {
        printf("Error: Division by zero!\n");
        return 0;
    }
    return a / b;
}

// Classic equations
int triangle_area(int base, int height) {
    int area = multiply(base, height);
    return area;
}

int average_speed(int distance, int time) {
    int avg_speed = divide(distance, time);
    return avg_speed;
}

int force(int mass, int acceleration) {
    int result_force = multiply(mass, acceleration);
    return result_force;
}

int pythagoras(int side1, int side2) {
    int hypotenuse_squared = add(multiply(side1, side1), multiply(side2, side2));
    return hypotenuse_squared;
}