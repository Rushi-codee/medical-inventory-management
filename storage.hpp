#ifndef STORAGE_HPP
#define STORAGE_HPP

#include <string>
#include "inventory.hpp"

class Storage
{
public:
    // static so can be called as Storage::save(...)
    static bool save(const Inventory &inv, const std::string &filename);
    static bool load(Inventory &inv, const std::string &filename);
};

#endif // STORAGE_HPP
