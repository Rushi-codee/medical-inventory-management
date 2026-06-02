#include "reports.hpp"
#include "inventory.hpp"
#include "medicine.hpp"
#include <fstream>
#include <iostream>
#include <iomanip>
#include <ctime>
#include <sstream>
#ifdef _WIN32
#include <direct.h>
#define make_dir(path) _mkdir(path)
#else
#include <sys/stat.h>
#define make_dir(path) mkdir(path, 0777)
#endif

void generateExpiredReport(const Inventory &inv)
{
    // Generate timestamp
    std::time_t now = std::time(nullptr);
    std::tm *tm_now = std::localtime(&now);
    std::stringstream ss;
    ss << "expired report_" << (tm_now->tm_year + 1900) << "-"
       << std::setfill('0') << std::setw(2) << (tm_now->tm_mon + 1) << "-"
       << std::setfill('0') << std::setw(2) << tm_now->tm_mday << "_"
       << std::setfill('0') << std::setw(2) << tm_now->tm_hour << "-"
       << std::setfill('0') << std::setw(2) << tm_now->tm_min << "-"
       << std::setfill('0') << std::setw(2) << tm_now->tm_sec << ".txt";
    make_dir("reports");
    std::string filename = "reports/" + ss.str();

    std::ofstream file(filename);
    if (!file.is_open())
    {
        std::cerr << "Error opening file: " << filename << std::endl;
        return;
    }

    auto expiredMedicines = inv.getExpired();

    file << "EXPIRED MEDICINES REPORT\n";
    file << "========================\n\n";
    file << "Generated on: " << std::ctime(&now);
    file << "Total expired medicines: " << expiredMedicines.size() << "\n\n";

    if (expiredMedicines.empty())
    {
        file << "No expired medicines found.\n";
    }
    else
    {
        file << std::left << std::setw(20) << "Name" << " | " << std::setw(8) << "Batch"
             << " | " << std::setw(10) << "Expiry" << " | " << std::setw(6) << "Qty"
             << " | " << std::setw(7) << "Price" << " | " << "Thr\n";
        file << std::string(80, '-') << "\n";
        for (const auto &med : expiredMedicines)
        {
            file << std::left << std::setw(20) << med.getName()
                 << " | " << std::setw(8) << med.getBatch()
                 << " | " << std::setw(10) << med.getExpiryString()
                 << " | " << std::setw(6) << med.getQuantity()
                 << " | " << std::setw(7) << med.getPrice()
                 << " | " << med.getThreshold() << "\n";
        }
    }

    file.close();
    std::cout << "Expired medicines report generated: " << filename << std::endl;
}

void generateLowStockReport(const Inventory &inv)
{
    // Generate timestamp
    std::time_t now = std::time(nullptr);
    std::tm *tm_now = std::localtime(&now);
    std::stringstream ss;
    ss << "lowstockreport_" << (tm_now->tm_year + 1900) << "-"
       << std::setfill('0') << std::setw(2) << (tm_now->tm_mon + 1) << "-"
       << std::setfill('0') << std::setw(2) << tm_now->tm_mday << "_"
       << std::setfill('0') << std::setw(2) << tm_now->tm_hour << "-"
       << std::setfill('0') << std::setw(2) << tm_now->tm_min << "-"
       << std::setfill('0') << std::setw(2) << tm_now->tm_sec << ".txt";
    make_dir("reports");
    std::string filename = "reports/" + ss.str();

    std::ofstream file(filename);
    if (!file.is_open())
    {
        std::cerr << "Error opening file: " << filename << std::endl;
        return;
    }

    auto lowStockMedicines = inv.getLowStock();

    file << "LOW STOCK MEDICINES REPORT\n";
    file << "==========================\n\n";
    file << "Generated on: " << std::ctime(&now);
    file << "Total low stock medicines: " << lowStockMedicines.size() << "\n\n";

    if (lowStockMedicines.empty())
    {
        file << "No low stock medicines found.\n";
    }
    else
    {
        file << std::left << std::setw(20) << "Name" << " | " << std::setw(8) << "Batch"
             << " | " << std::setw(10) << "Expiry" << " | " << std::setw(6) << "Qty"
             << " | " << std::setw(7) << "Price" << " | " << "Thr\n";
        file << std::string(80, '-') << "\n";
        for (const auto &med : lowStockMedicines)
        {
            file << std::left << std::setw(20) << med.getName()
                 << " | " << std::setw(8) << med.getBatch()
                 << " | " << std::setw(10) << med.getExpiryString()
                 << " | " << std::setw(6) << med.getQuantity()
                 << " | " << std::setw(7) << med.getPrice()
                 << " | " << med.getThreshold() << "\n";
        }
    }

    file.close();
    std::cout << "Low stock medicines report generated: " << filename << std::endl;
}
