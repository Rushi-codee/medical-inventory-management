#ifndef REPORTS_HPP
#define REPORTS_HPP

#include "inventory.hpp"
#include <string>

void generateExpiredReport(const Inventory& inv);
void generateLowStockReport(const Inventory& inv);

#endif // REPORTS_HPP
