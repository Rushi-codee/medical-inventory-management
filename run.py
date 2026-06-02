import subprocess
import sys
import os

def run_project():
    cpp_files = ["Main.cpp", "inventory.cpp", "medicine.cpp", "reports.cpp", "search.cpp", "storage.cpp", "date_utils.cpp", "login.cpp"]
    output_exe = "MedicalInventory.exe"

    print("====================================================")
    print("MIMS: Medical Inventory Management System Launcher")
    print("====================================================")
    print("\n[1/2] Checking C++ compiler and compiling backend...")
    
    # Check if C++ files exist before trying to compile
    missing_cpp = [f for f in cpp_files if not os.path.exists(f)]
    if missing_cpp:
        print(f"Warning: Missing source files for compilation: {', '.join(missing_cpp)}")
        print("Skipping compilation and trying to run existing executable...")
    else:
        try:
            # Check if g++ is installed
            result = subprocess.run(["g++", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print("g++ compiler found. Compiling...")
                compile_cmd = ["g++", "-std=c++17"] + cpp_files + ["-o", output_exe]
                compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
                if compile_result.returncode == 0:
                    print("Backend C++ compiled successfully!")
                else:
                    print("Compilation failed with errors:")
                    print(compile_result.stderr)
                    print("Will attempt to launch server with existing MedicalInventory.exe if it exists.")
            else:
                print("g++ failed to execute. Using existing MedicalInventory.exe...")
        except FileNotFoundError:
            print("g++ compiler not found in system PATH. Using existing MedicalInventory.exe...")
        except Exception as e:
            print(f"Compilation error: {e}. Using existing MedicalInventory.exe...")

    print("\n[2/2] Launching Python local web server...")
    gui_script = os.path.join("gui", "gui.py")
    if not os.path.exists(gui_script):
        print(f"Error: GUI script not found at {gui_script}")
        sys.exit(1)
        
    try:
        # Launch gui.py
        # Use sys.executable to run with the same python interpreter
        subprocess.run([sys.executable, gui_script])
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error launching server: {e}")

if __name__ == "__main__":
    run_project()
