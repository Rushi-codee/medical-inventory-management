# Medical Inventory Management System (MIMS)

MIMS is a robust, hybrid-architecture Medical Inventory Management System. It combines the high-performance data processing of a **C++ backend** with the modern, responsive user interface of a **web-based frontend** (HTML/Tailwind CSS/JS) served by a **Python backend server**.

<img width="1907" height="962" alt="image" src="https://github.com/user-attachments/assets/5b6644a2-f748-4ca6-8eeb-87d310d763a4" />


## Features

- **Dashboard & KPI Tracking**: Monitor total medicines, low stock items, expired inventory, and total stock valuation at a glance.
- **Inventory Directory**: A complete, filterable view of all medical stock with batch IDs, expiry dates, quantities, and pricing.
- **Low Stock & Expired Alerts**: Automatically tracks medicines that fall below custom thresholds or have passed their expiry dates.
- **Automated Reporting**: Generate, view, and manage reports for expired and low-stock items. Reports can be viewed directly in the app or downloaded as PDFs.
- **Context Operations Console**: 
  - Add new medicines with specific batch numbers and thresholds.
  - Update quantities (add/remove stock).
  - Modify expiry dates.
  - Delete expired or discontinued batches.
- **Hybrid Architecture**: Fast C++ executable for business logic and file-based data storage, linked to a beautiful Tailwind CSS web interface via a Python API bridge.

<img width="1918" height="952" alt="image" src="https://github.com/user-attachments/assets/2ed4e58e-e5a2-4f89-ad01-15716b5fcba3" />


## Technology Stack

- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (via CDN)
- **Middleware/Web Server**: Python (Local HTTP Server / API router)
- **Backend/Data Processing**: C++ (Compiled to `MedicalInventory.exe`)
- **PDF Generation**: jsPDF (Client-side)

## Project Structure

```text
├── run.py                 # Main launcher script (Compiles C++ & starts Python server)
├── MedicalInventory.exe   # Compiled C++ backend executable
├── Main.cpp, *.cpp, *.hpp # C++ source code files for core logic
├── data/                  # Data storage directory for inventory records
├── reports/               # Directory for generated .txt reports
├── gui/
│   ├── gui.py             # Python HTTP server that bridges frontend to C++ backend
│   └── web/
│       └── index.html     # Main frontend user interface
└── README.md              # This documentation file
```
<img width="397" height="692" alt="image" src="https://github.com/user-attachments/assets/dee7766b-17c3-4e46-ae37-44cffa140c6b" />


## Prerequisites

To run this application locally, you will need:
1. **Python 3.x** installed on your system.
2. **g++ compiler** (MinGW for Windows) installed and added to your system PATH (required to compile the C++ backend if making changes).

## Installation & Running

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rushi-codee/medical-inventory-management.git
   cd medical-inventory-management
   ```

2. **Launch the Application**:
   Run the `run.py` launcher script using Python:
   ```bash
   python run.py
   ```
   
   The `run.py` script will automatically:
   - Check for the C++ compiler (`g++`).
   - Compile the backend source files into `MedicalInventory.exe` (if not already compiled).
   - Launch the local Python web server (`gui.py`).

3. **Access the Web Portal**:
   Once the server starts, open your web browser and navigate to the address provided in your terminal (usually `http://localhost:8080`).

<img width="1902" height="893" alt="image" src="https://github.com/user-attachments/assets/e3496bd5-ee99-4aee-b8ca-cf7a74af607c" />
<img width="902" height="367" alt="image" src="https://github.com/user-attachments/assets/50b5c948-3691-4a48-be06-6fcb0bde0248" />


## Usage

1. **Login**: Use the admin credentials to log into the portal.
2. **Navigation**: Use the sidebar to filter views (All Medicines, Low Stock, Expired).
3. **Manage Stock**: Use the right-hand panel ("Console Operations") to Add, Update Quantity, Modify Expiry, or Delete records. 
4. **Generate Reports**: Click on "Generate Expired Report" or "Generate Low Stock Report" in the sidebar, then navigate to the "Report Directories" to view or download them.

<img width="1916" height="900" alt="image" src="https://github.com/user-attachments/assets/95ef9929-dccb-48e2-9fb8-ff3493751c6e" />

