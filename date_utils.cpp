#include "date_utils.hpp"
#include <ctime>
#include <sstream>
#include <iomanip>

using namespace std;
using namespace std::chrono;

bool parseDate(const string &dateStr, system_clock::time_point &out_tp)
{
    if (dateStr.size() != 10)
        return false;
    int Y, M, D;
    char c1, c2;
    istringstream iss(dateStr);
    iss >> Y >> c1 >> M >> c2 >> D;
    if (!iss || c1 != '-' || c2 != '-')
        return false;

    tm tm_t = {};
    tm_t.tm_year = Y - 1900;
    tm_t.tm_mon = M - 1;
    tm_t.tm_mday = D;
    tm_t.tm_hour = 0;
    tm_t.tm_min = 0;
    tm_t.tm_sec = 0;

    time_t tt = mktime(&tm_t);
    if (tt == -1)
        return false;
    out_tp = system_clock::from_time_t(tt);
    return true;
}

string formatDate(const system_clock::time_point &tp)
{
    time_t t = system_clock::to_time_t(tp);
    tm tm_t = *localtime(&t);
    ostringstream oss;
    oss << put_time(&tm_t, "%Y-%m-%d");
    return oss.str();
}

system_clock::time_point today()
{
    auto now = system_clock::now();
    time_t tt = system_clock::to_time_t(now);
    tm tm_t = *localtime(&tt);
    tm_t.tm_hour = 0;
    tm_t.tm_min = 0;
    tm_t.tm_sec = 0;
    return system_clock::from_time_t(mktime(&tm_t));
}
