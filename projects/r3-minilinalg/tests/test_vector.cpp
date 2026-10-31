#include <gtest/gtest.h>

#include "linalg/vector.h"

TEST(Vector, SizeAndAccess) {
  linalg::Vector v{1.0, 2.0, 3.0};
  EXPECT_EQ(v.size(), 3u);
  EXPECT_DOUBLE_EQ(v[0], 1.0);
  EXPECT_DOUBLE_EQ(v[2], 3.0);
}

TEST(Vector, Norm) {
  linalg::Vector v{3.0, 4.0};
  EXPECT_DOUBLE_EQ(v.norm(), 5.0);
}

TEST(Vector, Add) {
  linalg::Vector a{1.0, 2.0};
  linalg::Vector b{3.0, 4.0};
  linalg::Vector c = a + b;
  EXPECT_DOUBLE_EQ(c[0], 4.0);
  EXPECT_DOUBLE_EQ(c[1], 6.0);
}

TEST(Vector, AddMismatchThrows) {
  linalg::Vector a{1.0, 2.0};
  linalg::Vector b{1.0};
  EXPECT_THROW(a + b, std::invalid_argument);
}