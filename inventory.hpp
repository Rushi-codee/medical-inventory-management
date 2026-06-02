#ifndef INVENTORY_HPP
#define INVENTORY_HPP

#include "medicine.hpp"
#include <vector>
#include <string>

class Inventory {
public:
    Inventory() = default;

    void addMedicine(const Medicine &m);
    bool updateQuantity(const std::string &name, const std::string &batch, int delta);
    bool updateExpiry(const std::string &name, const std::string &batch,
                      const std::chrono::system_clock::time_point &newExpiry);
    void removeExpired();
    bool removeMedicine(const std::string &name, const std::string &batch);

    std::vector<Medicine> getExpired() const;
    std::vector<Medicine> getLowStock() const;
    void displayAll() const;

    // For storage
    const std::vector<Medicine>& getAll() const;
    void clear();

private:
    std::vector<Medicine> items_;
};

#endif // INVENTORY_HPP
