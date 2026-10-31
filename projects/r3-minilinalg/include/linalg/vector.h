#pragma once

#include <cstddef>
#include <initializer_list>
#include <vector>

namespace linalg {

class Vector {
 public:
  explicit Vector(std::size_t n);
  Vector(std::initializer_list<double> init);

  std::size_t size() const noexcept;

  double& operator[](std::size_t i);
  const double& operator[](std::size_t i) const;

  double norm() const;
  Vector operator+(const Vector& other) const;

 private:
  std::vector<double> data_;
};

}  // namespace linalg