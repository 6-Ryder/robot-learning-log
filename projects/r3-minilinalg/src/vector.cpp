#include "linalg/vector.h"

#include <cmath>
#include <stdexcept>

namespace linalg {

Vector::Vector(std::size_t n) : data_(n, 0.0) {}

Vector::Vector(std::initializer_list<double> init) : data_(init) {}

std::size_t Vector::size() const noexcept { return data_.size(); }

double& Vector::operator[](std::size_t i) { return data_.at(i); }

const double& Vector::operator[](std::size_t i) const { return data_.at(i); }

double Vector::norm() const {
  double sum = 0.0;
  for (double x : data_) {
    sum += x * x;
  }
  return std::sqrt(sum);
}

Vector Vector::operator+(const Vector& other) const {
  if (size() != other.size()) {
    throw std::invalid_argument("Vector::operator+: size mismatch");
  }
  Vector result(size());
  for (std::size_t i = 0; i < size(); ++i) {
    result[i] = data_[i] + other.data_[i];
  }
  return result;
}

}  // namespace linalg