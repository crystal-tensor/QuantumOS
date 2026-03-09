#include "../include/qhal_driver.hpp"
#include <iostream>

// Forward declaration from mock_driver.cpp
extern "C" qos::hal::IQHalDriver* create_mock_driver();

int main() {
    qos::hal::IQHalDriver* driver = create_mock_driver();
    
    if (driver->initialize()) {
        std::cout << "Driver initialized successfully: " << driver->get_name() << std::endl;
        
        driver->allocate_qubit(0);
        driver->allocate_qubit(1);
        
        driver->execute_u3(0, 1.57, 0.0, 3.14);
        driver->execute_wait(1, 100);
        driver->execute_cx(0, 1);
        driver->measure(0, 0);
        
        driver->free_qubit(0);
        driver->free_qubit(1);
    } else {
        std::cerr << "Driver initialization failed!" << std::endl;
        delete driver;
        return 1;
    }

    delete driver;
    return 0;
}
