#include <iostream>

#include "linalg/vector.h"

int main() {
  linalg::Vector a{1.0, 2.0, 3.0};
  linalg::Vector b{4.0, 5.0, 6.0};
  linalg::Vector c = a + b;

  std::cout << "a + b = [" << c[0] << ", " << c[1] << ", " << c[2] << "]\n";
  std::cout << "norm = " << c.norm() << "\n";
  return 0;
}