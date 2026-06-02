#include "inventory.hpp"
#include "date_utils.hpp"
#include <algorithm>
#include <iostream>
#include <iomanip>

using namespace std;
using namespace std::chrono;

void Inventory::addMedicine(const Medicine &m)
{
    items_.push_back(m);
}

bool Inventory::updateQuantity(const string &name, const string &batch, int delta)
{
    for (auto &m : items_)
    {
        if (m.getName() == name && m.getBatch() == batch)
        {
            int newQ = m.getQuantity() + delta;
            if (newQ < 0)
                newQ = 0;
            m.setQuantity(newQ);
            return true;
        }
    }
    return false;
}

bool Inventory::updateExpiry(const string &name, const string &batch,
                             const system_clock::time_point &newExpiry)
{
    for (auto &m : items_)
    {
        if (m.getName() == name && m.getBatch() == batch)
        {
            m.setExpiry(newExpiry);
            return true;
        }
    }
    return false;
}

void Inventory::removeExpired()
{
    items_.erase(remove_if(items_.begin(), items_.end(),
                           [](const Medicine &m)
                           { return m.isExpired(); }),
                 items_.end());
}

bool Inventory::removeMedicine(const string &name, const string &batch)
{
    auto it = remove_if(items_.begin(), items_.end(),
                        [&](const Medicine &m)
                        { return m.getName() == name && m.getBatch() == batch; });
    if (it != items_.end())
    {
        items_.erase(it, items_.end());
        return true;
    }
    return false;
}

vector<Medicine> Inventory::getExpired() const
{
    vector<Medicine> out;
    for (const auto &m : items_)
        if (m.isExpired())
            out.push_back(m);
    return out;
}

vector<Medicine> Inventory::getLowStock() const
{
    vector<Medicine> out;
    for (const auto &m : items_)
        if (m.getQuantity() <= m.getThreshold())
            out.push_back(m);
    return out;
}

void Inventory::displayAll() const
{
    cout << "\n------------------- INVENTORY -------------------\n";
    cout << left << setw(20) << "Name" << " | " << setw(8) << "Batch"
         << " | " << setw(10) << "Expiry" << " | " << setw(6) << "Qty"
         << " | " << setw(7) << "Price" << " | " << "Thr\n";
    cout << string(80, '-') << "\n";
    for (const auto &m : items_)
        m.display();
}

const vector<Medicine> &Inventory::getAll() const { return items_; }
void Inventory::clear() { items_.clear(); }
