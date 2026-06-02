#ifndef DATE_UTILS_HPP
#define DATE_UTILS_HPP

#include <string>
#include <chrono>

// Parse "YYYY-MM-DD" -> time_point. Returns true on success.
bool parseDate(const std::string &dateStr, std::chrono::system_clock::time_point &out_tp);

// Format time_point -> "YYYY-MM-DD"
std::string formatDate(const std::chrono::system_clock::time_point &tp);

// Return today's date at midnight local time
std::chrono::system_clock::time_point today();

#endif // DATE_UTILS_HPP
