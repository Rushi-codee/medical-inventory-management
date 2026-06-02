#include "search.hpp"
#include "date_utils.hpp"
#include <algorithm>
#include <cctype>

using namespace std;

// Helper function to convert string to lowercase
string toLower(const string &str)
{
    string lowerStr = str;
    transform(lowerStr.begin(), lowerStr.end(), lowerStr.begin(), ::tolower);
    return lowerStr;
}

// Search by name (case-insensitive partial match)
vector<Medicine> searchByName(const Inventory &inv, const string &name)
{
    vector<Medicine> results;
    string lowerName = toLower(name);
    for (const auto &med : inv.getAll())
    {
        if (toLower(med.getName()).find(lowerName) != string::npos)
        {
            results.push_back(med);
        }
    }
    return results;
}

// Search by batch (case-insensitive partial match)
vector<Medicine> searchByBatch(const Inventory &inv, const string &batch)
{
    vector<Medicine> results;
    string lowerBatch = toLower(batch);
    for (const auto &med : inv.getAll())
    {
        if (toLower(med.getBatch()).find(lowerBatch) != string::npos)
        {
            results.push_back(med);
        }
    }
    return results;
}

// Search by expiry month (format: YYYY-MM)
vector<Medicine> searchByExpiryMonth(const Inventory &inv, const string &month)
{
    vector<Medicine> results;
    for (const auto &med : inv.getAll())
    {
        string expiryStr = med.getExpiryString();
        // Extract year-month from YYYY-MM-DD
        if (expiryStr.length() >= 7)
        {
            string medMonth = expiryStr.substr(0, 7); // YYYY-MM
            if (medMonth == month)
            {
                results.push_back(med);
            }
        }
    }
    return results;
}
