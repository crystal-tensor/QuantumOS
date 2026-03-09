#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace qos::hal {

    /**
     * @brief Abstract base class for Quantum Hardware Abstraction Layer (Q-HAL).
     * 
     * This interface defines the standard operations that any quantum backend
     * (superconducting, ion trap, or simulator) must implement to be compatible
     * with QuantumOS.
     */
    class IQHalDriver {
    public:
        virtual ~IQHalDriver() = default;

        /**
         * @brief Initialize the hardware connection.
         * @return true if initialization is successful, false otherwise.
         */
        virtual bool initialize() = 0;

        /**
         * @brief Allocate a physical qubit.
         * @param qubit_id Physical qubit index.
         * @return true if allocation is successful.
         */
        virtual bool allocate_qubit(uint32_t qubit_id) = 0;

        /**
         * @brief Free a physical qubit.
         * @param qubit_id Physical qubit index.
         * @return true if deallocation is successful.
         */
        virtual bool free_qubit(uint32_t qubit_id) = 0;

        /**
         * @brief Execute a single-qubit U3 gate.
         * 
         * U3(theta, phi, lambda) = 
         * [ cos(theta/2)          -e^(i*lambda) * sin(theta/2) ]
         * [ e^(i*phi) * sin(theta/2)  e^(i*(phi+lambda)) * cos(theta/2) ]
         * 
         * @param qubit_id Target qubit index.
         * @param theta Euler angle theta (radians).
         * @param phi Euler angle phi (radians).
         * @param lambda Euler angle lambda (radians).
         * @return true if execution is successful.
         */
        virtual bool execute_u3(uint32_t qubit_id, double theta, double phi, double lambda) = 0;

        /**
         * @brief Execute a Controlled-NOT (CX) gate.
         * 
         * @param ctrl_qubit_id Control qubit index.
         * @param target_qubit_id Target qubit index.
         * @return true if execution is successful.
         */
        virtual bool execute_cx(uint32_t ctrl_qubit_id, uint32_t target_qubit_id) = 0;

        /**
         * @brief Measure a qubit in the Z-basis.
         * 
         * @param qubit_id Target qubit index.
         * @param cl_reg_id Classical register index to store the result.
         * @return true if measurement command is successfully dispatched.
         */
        virtual bool measure(uint32_t qubit_id, uint32_t cl_reg_id) = 0;

        /**
         * @brief Wait for a specified duration (Time-Aware).
         * 
         * Forces the qubit to idle for `duration_ns`.
         * 
         * @param qubit_id Target qubit index.
         * @param duration_ns Wait time in nanoseconds.
         * @return true if wait command is successfully dispatched.
         */
        virtual bool execute_wait(uint32_t qubit_id, uint64_t duration_ns) = 0;

        /**
         * @brief Get the name of the driver.
         * @return Driver name string.
         */
        virtual std::string get_name() const = 0;
    };

} // namespace qos::hal
