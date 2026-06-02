#include "login.hpp"
#include <iostream>
#include <fstream>
#include <string>
#include <limits>

using namespace std;

bool authenticateUser()
{
    string username, password;
    string storedUsername, storedPassword;

    // Read credentials from auth.txt
    ifstream authFile("auth.txt");
    if (!authFile.is_open())
    {
        cout << "Error: Unable to open auth.txt file.\n";
        return false;
    }

    getline(authFile, storedUsername, ',');
    getline(authFile, storedPassword);
    authFile.close();

    // Prompt for username and password
    cout << "Enter admin username: ";
    getline(cin, username);

    cout << "Enter password: ";
    getline(cin, password);

    // Check if entered credentials match stored ones
    if (username == storedUsername && password == storedPassword)
    {
        cout << "Authentication successful!\n";
        return true;
    }
    else
    {
        cout << "Authentication failed. Invalid username or password.\n";
        return false;
    }
}

bool authenticateUser(string username, string password)
{
    string storedUsername, storedPassword;

    // Read credentials from auth.txt
    ifstream authFile("auth.txt");
    if (!authFile.is_open())
    {
        cout << "Error: Unable to open auth.txt file.\n";
        return false;
    }

    getline(authFile, storedUsername, ',');
    getline(authFile, storedPassword);
    authFile.close();

    // Trim trailing whitespace/newlines from storedPassword
    size_t end = storedPassword.find_last_not_of(" \t\n\r\f\v");
    if (end != string::npos)
        storedPassword = storedPassword.substr(0, end + 1);
    else
        storedPassword.clear(); // all whitespace

    // Check if entered credentials match stored ones
    if (username == storedUsername && password == storedPassword)
    {
        return true;
    }
    else
    {
        return false;
    }
}
