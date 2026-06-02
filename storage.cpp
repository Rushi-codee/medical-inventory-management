#include "storage.hpp"
#include <fstream>
#include <iostream>

using namespace std;

bool Storage::save(const Inventory &inv, const string &filename)
{
    ofstream ofs(filename);
    if (!ofs)
        return false;
    ofs << "name,batch,expiry,qty,price,threshold\n";
    for (const auto &m : inv.getAll())
    {
        ofs << m.toCSV() << '\n';
    }
    return true;
}

bool Storage::load(Inventory &inv, const string &filename)
{
    ifstream ifs(filename);
    if (!ifs)
        return false;
    inv.clear();
    string line;
    // Read header (if present)
    if (!getline(ifs, line))
        return true; // empty file ok
    // If header doesn't match, we'll still try to parse lines below
    while (getline(ifs, line))
    {
        if (line.size() < 3)
            continue;
        Medicine m = Medicine::fromCSV(line);
        inv.addMedicine(m);
    }
    return true;
}
