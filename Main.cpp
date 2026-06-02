// Main.cpp
#include <iostream>
#include <string>
#include <iomanip>
#include <limits>

#include "inventory.hpp"
#include "storage.hpp"
#include "date_utils.hpp"
#include "reports.hpp"
#include "login.hpp"
#include "search.hpp"

using namespace std;
using namespace std::chrono;

#define RESET "\033[0m"
#define GREEN "\033[32m"
#define YELLOW "\033[33m"
#define CYAN "\033[36m"
#define RED "\033[31m"
#define BOLD "\033[1m"

void waitForEnter()
{
    cout << "\nPress ENTER to continue...";
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cin.get();
}

void clearScreen()
{
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void uiAddMedicine(Inventory &inv)
{
    string name, batch, expiryStr;
    int qty = 0, thr = 0;
    double price = 0.0;
    const string defaultFile = "data/inventory.csv";

    cout << CYAN << "\n--- Add Medicine ---\n"
         << RESET;
    cout << "Name: ";
    cin >> ws;
    getline(cin, name);
    cout << "Batch: ";
    cin >> ws;
    getline(cin, batch);
    cout << "Expiry (YYYY-MM-DD): ";
    cin >> expiryStr;
    system_clock::time_point tp;
    if (!parseDate(expiryStr, tp))
    {
        cout << RED << "Invalid date format. Aborting.\n"
             << RESET;
        return;
    }
    cout << "Quantity: ";
    if (!(cin >> qty))
    {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "Bad input\n";
        return;
    }
    cout << "Price: ";
    if (!(cin >> price))
    {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "Bad input\n";
        return;
    }
    cout << "Threshold: ";
    if (!(cin >> thr))
    {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "Bad input\n";
        return;
    }
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    inv.addMedicine(Medicine(name, batch, tp, qty, price, thr));
    cout << GREEN << "Added.\n"
         << RESET;
    Storage::save(inv, defaultFile); // autosave
}

void uiUpdateQuantity(Inventory &inv)
{
    string name, batch;
    int delta;
    const string defaultFile = "data/inventory.csv";
    cout << CYAN << "\n--- Update Quantity ---\n"
         << RESET;
    cout << "Name: ";
    cin >> ws;
    getline(cin, name);
    cout << "Batch: ";
    cin >> ws;
    getline(cin, batch);
    cout << "Delta (+/-): ";
    if (!(cin >> delta))
    {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "Bad input\n";
        return;
    }
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    if (inv.updateQuantity(name, batch, delta))
    {
        cout << GREEN << "Updated.\n"
             << RESET;
        Storage::save(inv, defaultFile); // autosave
    }
    else
        cout << RED << "Not found.\n"
             << RESET;
}

void uiUpdateExpiry(Inventory &inv)
{
    string name, batch, expiryStr;
    const string defaultFile = "data/inventory.csv";
    cout << CYAN << "\n--- Update Expiry ---\n"
         << RESET;
    cout << "Name: ";
    cin >> ws;
    getline(cin, name);
    cout << "Batch: ";
    cin >> ws;
    getline(cin, batch);
    cout << "New expiry (YYYY-MM-DD): ";
    cin >> expiryStr;
    system_clock::time_point tp;
    if (!parseDate(expiryStr, tp))
    {
        cout << RED << "Invalid date.\n"
             << RESET;
        return;
    }
    if (inv.updateExpiry(name, batch, tp))
    {
        cout << GREEN << "Updated.\n"
             << RESET;
        Storage::save(inv, defaultFile); // autosave
    }
    else
        cout << RED << "Not found.\n"
             << RESET;
}

void uiDeleteMedicine(Inventory &inv)
{
    string name, batch;
    cout << CYAN << "\n--- Delete Medicine ---\n"
         << RESET;
    cout << "Name: ";
    cin >> ws;
    getline(cin, name);
    cout << "Batch: ";
    cin >> ws;
    getline(cin, batch);
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    if (inv.removeMedicine(name, batch))
    {
        cout << GREEN << "Deleted.\n"
             << RESET;
        Storage::save(inv, "data/inventory.csv"); // autosave
    }
    else
        cout << RED << "Not found.\n"
             << RESET;
}

void uiSearchMedicines(const Inventory &inv)
{
    cout << CYAN << "\n--- Search Medicines ---\n"
         << RESET;
    cout << "Search by:\n";
    cout << "1. Name\n";
    cout << "2. Batch\n";
    cout << "3. Expiry Month (YYYY-MM)\n";
    cout << "Choice: ";
    int searchChoice;
    if (!(cin >> searchChoice))
    {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << RED << "Invalid input\n"
             << RESET;
        return;
    }
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    vector<Medicine> results;
    string query;

    switch (searchChoice)
    {
    case 1:
        cout << "Enter medicine name: ";
        getline(cin, query);
        results = searchByName(inv, query);
        break;
    case 2:
        cout << "Enter batch: ";
        getline(cin, query);
        results = searchByBatch(inv, query);
        break;
    case 3:
        cout << "Enter expiry month (YYYY-MM): ";
        getline(cin, query);
        results = searchByExpiryMonth(inv, query);
        break;
    default:
        cout << RED << "Invalid choice\n"
             << RESET;
        return;
    }

    if (results.empty())
    {
        cout << "No medicines found.\n";
    }
    else
    {
        cout << GREEN << "Found " << results.size() << " medicine(s):\n"
             << RESET;
        for (const auto &med : results)
        {
            med.display();
        }
    }
}

void cmdAddMedicine(Inventory &inv, int argc, char* argv[])
{
    if (argc < 7) {
        cout << RED << "Usage: add <name> <batch> <expiry> <qty> <price> <threshold>\n" << RESET;
        return;
    }
    string name = argv[2];
    string batch = argv[3];
    string expiryStr = argv[4];
    int qty = stoi(argv[5]);
    double price = stod(argv[6]);
    int thr = stoi(argv[7]);

    system_clock::time_point tp;
    if (!parseDate(expiryStr, tp)) {
        cout << RED << "Invalid date format.\n" << RESET;
        return;
    }

    inv.addMedicine(Medicine(name, batch, tp, qty, price, thr));
    cout << GREEN << "Added.\n" << RESET;
    Storage::save(inv, "data/inventory.csv");
}

void cmdUpdateQuantity(Inventory &inv, int argc, char* argv[])
{
    if (argc < 5) {
        cout << RED << "Usage: update_qty <name> <batch> <delta>\n" << RESET;
        return;
    }
    string name = argv[2];
    string batch = argv[3];
    int delta = stoi(argv[4]);

    if (inv.updateQuantity(name, batch, delta)) {
        cout << GREEN << "Updated.\n" << RESET;
        Storage::save(inv, "data/inventory.csv");
    } else {
        cout << RED << "Not found.\n" << RESET;
    }
}

void cmdUpdateExpiry(Inventory &inv, int argc, char* argv[])
{
    if (argc < 5) {
        cout << RED << "Usage: update_expiry <name> <batch> <expiry>\n" << RESET;
        return;
    }
    string name = argv[2];
    string batch = argv[3];
    string expiryStr = argv[4];

    system_clock::time_point tp;
    if (!parseDate(expiryStr, tp)) {
        cout << RED << "Invalid date.\n" << RESET;
        return;
    }

    if (inv.updateExpiry(name, batch, tp)) {
        cout << GREEN << "Updated.\n" << RESET;
        Storage::save(inv, "data/inventory.csv");
    } else {
        cout << RED << "Not found.\n" << RESET;
    }
}

void cmdRemoveExpired(Inventory &inv)
{
    inv.removeExpired();
    cout << GREEN << "Removed expired items.\n" << RESET;
    Storage::save(inv, "data/inventory.csv");
}

void cmdDisplayAll(Inventory &inv)
{
    inv.displayAll();
}

void cmdShowExpired(Inventory &inv)
{
    auto v = inv.getExpired();
    if (v.empty()) {
        cout << "No expired items.\n";
    } else {
        for (auto &m : v) {
            m.display();
        }
    }
}

void cmdShowLowStock(Inventory &inv)
{
    auto v = inv.getLowStock();
    if (v.empty()) {
        cout << "No low stock items.\n";
    } else {
        for (auto &m : v) {
            m.display();
        }
    }
}

void cmdSearchMedicines(Inventory &inv, int argc, char* argv[])
{
    if (argc < 3) {
        cout << RED << "Usage: search <name>\n" << RESET;
        return;
    }
    string name = argv[2];
    // Assuming search by name, you can modify to search by batch or other criteria
    auto results = searchByName(inv, name);
    if (results.empty()) {
        cout << "No medicines found with name: " << name << "\n";
    } else {
        for (const auto &m : results) {
            m.display();
        }
    }
}

void cmdDeleteMedicine(Inventory &inv, int argc, char* argv[])
{
    if (argc < 4) {
        cout << RED << "Usage: delete_medicine <name> <batch>\n" << RESET;
        return;
    }
    string name = argv[2];
    string batch = argv[3];

    if (inv.removeMedicine(name, batch)) {
        cout << GREEN << "Deleted.\n" << RESET;
        Storage::save(inv, "data/inventory.csv");
    } else {
        cout << RED << "Not found.\n" << RESET;
    }
}

void cmdGenerateExpiredReport(Inventory &inv)
{
    generateExpiredReport(inv);
}

void cmdGenerateLowStockReport(Inventory &inv)
{
    generateLowStockReport(inv);
}

int main(int argc, char* argv[])
{
    Inventory inv;
    const string defaultFile = "data/inventory.csv";

    // Try auto-load if file exists
    Storage::load(inv, defaultFile);

    if (argc > 1) {
        // Command-line mode
        string cmd = argv[1];
        if (cmd == "add") {
            cmdAddMedicine(inv, argc, argv);
        } else if (cmd == "update_qty") {
            cmdUpdateQuantity(inv, argc, argv);
        } else if (cmd == "update_expiry") {
            cmdUpdateExpiry(inv, argc, argv);
        } else if (cmd == "remove_expired") {
            cmdRemoveExpired(inv);
        } else if (cmd == "display_all") {
            cmdDisplayAll(inv);
        } else if (cmd == "show_expired") {
            cmdShowExpired(inv);
        } else if (cmd == "show_low_stock") {
            cmdShowLowStock(inv);
        } else if (cmd == "generate_expired_report") {
            cmdGenerateExpiredReport(inv);
        } else if (cmd == "generate_low_stock_report") {
            cmdGenerateLowStockReport(inv);
        } else if (cmd == "delete_medicine") {
            cmdDeleteMedicine(inv, argc, argv);
        } else if (cmd == "search") {
            cmdSearchMedicines(inv, argc, argv);
        } else if (cmd == "authenticate") {
            if (argc < 4) {
                cout << RED << "Usage: authenticate <username> <password>\n" << RESET;
                return 1;
            }
            if (authenticateUser(argv[2], argv[3])) {
                cout << "Authentication successful!" << endl;
            } else {
                cout << "Authentication failed." << endl;
            }
        } else {
            cout << RED << "Unknown command.\n" << RESET;
        }
        return 0;
    }

    // Interactive mode
    // Authenticate user before proceeding
    if (!authenticateUser())
    {
        cout << "Authentication failed. Exiting program.\n";
        return 1;
    }

    while (true)
    {
        clearScreen();
        cout << BOLD << CYAN;
        cout << "========================================\n";
        cout << "    MEDICAL INVENTORY MANAGEMENT\n";
        cout << "========================================\n"
             << RESET;

        cout << YELLOW
             << "1. Add Medicine\n"
             << "2. Update Quantity\n"
             << "3. Update Expiry\n"
             << "4. Remove Expired Medicines\n"
             << "5. Show All Medicines\n"
             << "6. Show Expired Medicines\n"
             << "7. Show Low Stock Medicines\n"
             << "8. Delete Medicine\n"
             << "9. Generate Expired Report\n"
             << "10. Generate Low Stock Report\n"
             << "11. Search Medicines\n"
             << "0. Exit\n"
             << RESET;

        cout << "Choice: ";
        int ch;
        if (!(cin >> ch))
        {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << RED << "Invalid input\n"
                 << RESET;
            waitForEnter();
            continue;
        }
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        switch (ch)
        {
        case 1:
            uiAddMedicine(inv);
            break;
        case 2:
            uiUpdateQuantity(inv);
            break;
        case 3:
            uiUpdateExpiry(inv);
            break;
        case 4:
            inv.removeExpired();
            cout << GREEN << "Removed expired items.\n"
                 << RESET;
            Storage::save(inv, defaultFile); // autosave
            break;
        case 5:
            inv.displayAll();
            break;
        case 6:
        {
            auto v = inv.getExpired();
            if (v.empty())
                cout << "No expired items.\n";
            else
                for (auto &m : v)
                    m.display();
            break;
        }
        case 7:
        {
            auto v = inv.getLowStock();
            if (v.empty())
                cout << "No low stock items.\n";
            else
                for (auto &m : v)
                    m.display();
            break;
        }
        case 8:
            uiDeleteMedicine(inv);
            break;
        case 9:
            generateExpiredReport(inv);
            break;
        case 10:
            generateLowStockReport(inv);
            break;
        case 11:
            uiSearchMedicines(inv);
            break;
        case 0:
            // auto-save on exit (optional)
            Storage::save(inv, defaultFile);
            cout << "Goodbye!\n";
            return 0;
        default:
            cout << RED << "Invalid choice\n"
                 << RESET;
        }

        waitForEnter();
    }

    return 0;
}
