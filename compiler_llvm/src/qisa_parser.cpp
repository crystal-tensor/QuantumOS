#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Verifier.h"
#include "llvm/Support/raw_ostream.h"
#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace llvm;

int main() {
    // 1. Setup LLVM Context and Module
    LLVMContext Context;
    std::unique_ptr<Module> TheModule = std::make_unique<Module>("QISA_Module", Context);
    IRBuilder<> Builder(Context);

    // 2. Define external quantum intrinsic types
    // %Qubit = type opaque
    // StructType *QubitType = StructType::create(Context, "Qubit");
    // %Qubit* -> ptr (opaque pointer in modern LLVM)
    PointerType *QubitPtrType = PointerType::get(Context, 0);

    // Declare external function: void @__quantum__qis__u3__body(double, double, double, %Qubit*)
    std::vector<Type*> U3ArgTypes = {
        Type::getDoubleTy(Context),
        Type::getDoubleTy(Context),
        Type::getDoubleTy(Context),
        QubitPtrType
    };
    FunctionType *U3FuncType = FunctionType::get(Type::getVoidTy(Context), U3ArgTypes, false);
    Function *U3Func = Function::Create(U3FuncType, Function::ExternalLinkage, "__quantum__qis__u3__body", TheModule.get());

    // Declare runtime function to get qubit by ID: %Qubit* @__quantum__rt__qubit_get_by_id(i64)
    std::vector<Type*> GetQubitArgTypes = { Type::getInt64Ty(Context) };
    FunctionType *GetQubitFuncType = FunctionType::get(QubitPtrType, GetQubitArgTypes, false);
    Function *GetQubitFunc = Function::Create(GetQubitFuncType, Function::ExternalLinkage, "__quantum__rt__qubit_get_by_id", TheModule.get());

    // 3. Create a main function to hold the instructions
    // define i32 @main()
    FunctionType *MainFuncType = FunctionType::get(Type::getInt32Ty(Context), false);
    Function *MainFunc = Function::Create(MainFuncType, Function::ExternalLinkage, "main", TheModule.get());
    
    BasicBlock *EntryBB = BasicBlock::Create(Context, "entry", MainFunc);
    Builder.SetInsertPoint(EntryBB);

    // 4. Parse the hardcoded string: "U3 1.57 0 3.14 q[0]"
    std::string qisa_cmd = "U3 1.57 0 3.14 q[0]";
    std::stringstream ss(qisa_cmd);
    
    std::string opcode;
    double theta, phi, lambda;
    std::string qreg_str;
    
    // Simple parsing logic
    // Assuming format: Opcode Arg1 Arg2 Arg3 Target
    if (ss >> opcode >> theta >> phi >> lambda >> qreg_str) {
        // Parse q[0] -> index 0
        int q_idx = 0;
        size_t start_bracket = qreg_str.find('[');
        size_t end_bracket = qreg_str.find(']');
        if (start_bracket != std::string::npos && end_bracket != std::string::npos) {
            std::string num_str = qreg_str.substr(start_bracket + 1, end_bracket - start_bracket - 1);
            try {
                q_idx = std::stoi(num_str);
            } catch (...) {
                std::cerr << "Error parsing qubit index\n";
                return 1;
            }
        }

        // 5. Generate LLVM IR
        if (opcode == "U3") {
            // Call get_qubit to resolve q[idx] to %Qubit*
            Value *QubitIdxVal = ConstantInt::get(Type::getInt64Ty(Context), q_idx);
            Value *QubitPtr = Builder.CreateCall(GetQubitFunc, {QubitIdxVal});

            // Prepare arguments for U3 call
            Value *ThetaVal = ConstantFP::get(Type::getDoubleTy(Context), theta);
            Value *PhiVal = ConstantFP::get(Type::getDoubleTy(Context), phi);
            Value *LambdaVal = ConstantFP::get(Type::getDoubleTy(Context), lambda);
            
            // Call U3
            Builder.CreateCall(U3Func, {ThetaVal, PhiVal, LambdaVal, QubitPtr});
        }
    } else {
        std::cerr << "Failed to parse command string\n";
        return 1;
    }

    // Return 0
    Builder.CreateRet(ConstantInt::get(Type::getInt32Ty(Context), 0));

    // 6. Print to stdout
    TheModule->print(outs(), nullptr);

    return 0;
}
