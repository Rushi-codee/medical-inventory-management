#include "medicine.hpp"
#include "date_utils.hpp"
#include <iostream>
#include <sstream>
#include <iomanip>

using namespace std;
using namespace std::chrono;

Medicine::Medicine(const string &name, const string &batch,
                   const system_clock::time_point &expiry,
                   int quantity, double price, int threshold)
    : name_(name), batch_(batch), expiry_(expiry),
      quantity_(quantity), price_(price), threshold_(threshold) {}

string Medicine::getName() const { return name_; }
string Medicine::getBatch() const { return batch_; }
system_clock::time_point Medicine::getExpiry() const { return expiry_; }
int Medicine::getQuantity() const { return quantity_; }
double Medicine::getPrice() const { return price_; }
int Medicine::getThreshold() const { return threshold_; }

void Medicine::setQuantity(int q) { quantity_ = q; }
void Medicine::setExpiry(const system_clock::time_point &tp) { expiry_ = tp; }

bool Medicine::isExpired() const
{
  return expiry_ <= today();
}

string Medicine::getExpiryString() const
{
  return formatDate(expiry_);
}

void Medicine::display() const
{
  cout << left;
  cout << setw(20) << name_
       << " | " << setw(8) << batch_
       << " | " << setw(10) << getExpiryString()
       << " | Qty: " << setw(4) << quantity_
       << " | Price: " << setw(7) << price_
       << " | Thr: " << threshold_
       << "\n";
}

string Medicine::toCSV() const
{
  ostringstream ss;
  ss << name_ << ',' << batch_ << ',' << getExpiryString() << ','
     << quantity_ << ',' << price_ << ',' << threshold_;
  return ss.str();
}

Medicine Medicine::fromCSV(const string &line)
{
  // Expect: name,batch,expiry,qty,price,threshold
  stringstream ss(line);
  string name, batch, expiryStr, qtyStr, priceStr, thStr;

  getline(ss, name, ',');
  getline(ss, batch, ',');
  getline(ss, expiryStr, ',');
  getline(ss, qtyStr, ',');
  getline(ss, priceStr, ',');
  getline(ss, thStr, ',');

  int qty = 0, th = 0;
  double price = 0.0;
  try
  {
    if (!qtyStr.empty())
      qty = stoi(qtyStr);
    if (!priceStr.empty())
      price = stod(priceStr);
    if (!thStr.empty())
      th = stoi(thStr);
  }
  catch (...)
  {
    // keep defaults
  }

  system_clock::time_point exp = system_clock::now();
  parseDate(expiryStr, exp); // if fails, exp becomes now()

  return Medicine(name, batch, exp, qty, price, th);
}
