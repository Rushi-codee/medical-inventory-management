#ifndef MEDICINE_HPP
#define MEDICINE_HPP

#include <string>
#include <chrono>

class Medicine
{
public:
    Medicine() = default;
    Medicine(const std::string &name,
             const std::string &batch,
             const std::chrono::system_clock::time_point &expiry,
             int quantity,
             double price,
             int threshold);

    // getters
    std::string getName() const;
    std::string getBatch() const;
    std::string getExpiryString() const;
    std::chrono::system_clock::time_point getExpiry() const;
    int getQuantity() const;
    double getPrice() const;
    int getThreshold() const;

    // setters
    void setQuantity(int q);
    void setExpiry(const std::chrono::system_clock::time_point &tp);

    // logic
    bool isExpired() const;

    // UI & CSV helpers
    void display() const;
    std::string toCSV() const;
    static Medicine fromCSV(const std::string &line);

private:
    std::string name_;
    std::string batch_;
    std::chrono::system_clock::time_point expiry_;
    int quantity_{0};
    double price_{0.0};
    int threshold_{0};
};

#endif // MEDICINE_HPP
