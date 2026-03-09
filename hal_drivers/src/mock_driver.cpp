#include "../include/qhal_driver.hpp"
#include <iostream>
#include <iomanip>
#include <string>

namespace qos::hal {

    /**
     * @brief A Mock implementation of the Q-HAL driver for testing and simulation purposes.
     * 
     * This driver simply logs all commands to stdout.
     */
    class MockDriver : public IQHalDriver {
    public:
        MockDriver() {
            std::cout << "[MockDriver] Instance created." << std::endl;
        }

        bool initialize() override {
            std::cout << "[MockDriver] Initializing mock hardware connection..." << std::endl;
            return true;
        }

        bool allocate_qubit(uint32_t qubit_id) override {
            std::cout << "[MockDriver] QALLOC q[" << qubit_id << "]" << std::endl;
            return true;
        }

        bool free_qubit(uint32_t qubit_id) override {
            std::cout << "[MockDriver] QFREE q[" << qubit_id << "]" << std::endl;
            return true;
        }

        bool execute_u3(uint32_t qubit_id, double theta, double phi, double lambda) override {
            std::cout << "[MockDriver] U3(" 
                      << std::fixed << std::setprecision(4) << theta << ", " 
                      << phi << ", " 
                      << lambda << ") -> q[" << qubit_id << "]" << std::endl;
            return true;
        }

        bool execute_cx(uint32_t ctrl_qubit_id, uint32_t target_qubit_id) override {
            std::cout << "[MockDriver] CX q[" << ctrl_qubit_id << "] -> q[" << target_qubit_id << "]" << std::endl;
            return true;
        }

        bool measure(uint32_t qubit_id, uint32_t cl_reg_id) override {
            std::cout << "[MockDriver] MEASURE q[" << qubit_id << "] -> c[" << cl_reg_id << "]" << std::endl;
            return true;
        }

        bool execute_wait(uint32_t qubit_id, uint64_t duration_ns) override {
            std::cout << "[MockDriver] WAIT " << duration_ns << "ns -> q[" << qubit_id << "]" << std::endl;
            return true;
        }

        std::string get_name() const override {
            return "MockQuantumDriver-v0.1";
        }
    };

} // namespace qos::hal

// Export a factory function if needed (for shared library usage)
extern "C" {
    qos::hal::IQHalDriver* create_mock_driver() {
        return new qos::hal::MockDriver();
    }
}
