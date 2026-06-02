#ifndef SEARCH_HPP
#define SEARCH_HPP

#include "inventory.hpp"
#include <vector>
#include <string>

// Function to search medicines by name
std::vector<Medicine> searchByName(const Inventory &inv, const std::string &name);

// Function to search medicines by batch
std::vector<Medicine> searchByBatch(const Inventory &inv, const std::string &batch);

// Function to search medicines by expiry month (YYYY-MM)
std::vector<Medicine> searchByExpiryMonth(const Inventory &inv, const std::string &month);

#endif // SEARCH_HPP
