import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import matplotlib.font_manager as fm
import numpy as np

# Set Chinese font
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_vqe_workflow():
    fig = plt.figure(figsize=(24, 14), constrained_layout=True)
    gs = GridSpec(2, 4, figure=fig, height_ratios=[1, 1.2])
    
    # Define colors
    c_user = "#E3F2FD" # Blue 50
    c_comp = "#F3E5F5" # Purple 50
    c_kern = "#E8F5E9" # Green 50
    c_qec  = "#FFEBEE" # Red 50
    c_hw   = "#FFF3E0" # Orange 50
    c_border = "#333333"

    # =========================================================================
    # Panel 1: User Code & VQE Circuit (Ansatz) - 4 Qubits
    # =========================================================================
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title("1. 用户层: VQE 算法 (4 Qubit H2)", fontsize=14, pad=10, fontweight='bold')
    ax1.axis('off')
    
    # Code box
    rect1 = patches.Rectangle((0.05, 0.65), 0.9, 0.3, linewidth=1, edgecolor=c_border, facecolor=c_user)
    ax1.add_patch(rect1)
    ax1.text(0.07, 0.92, "Python SDK (VQE - HEA):", fontsize=10, fontweight='bold', va='top')
    code_text = """def ansatz(theta):
    q = QuantumRegister(4)
    for i in range(4):
        circuit.ry(theta[i], q[i])
    # Entanglement
    circuit.cx(q[0], q[1])
    circuit.cx(q[1], q[2])
    circuit.cx(q[2], q[3])
    circuit.cx(q[3], q[0])
    # Layer 2
    for i in range(4):
        circuit.ry(theta[i+4], q[i])
    return circuit"""
    ax1.text(0.07, 0.88, code_text, fontsize=8, family='monospace', va='top')
    
    # Circuit Diagram
    ax1.text(0.1, 0.58, "量子电路 (Hardware Efficient):", fontsize=10, fontweight='bold')
    
    y_lines = [0.5, 0.4, 0.3, 0.2]
    labels = ["q[0]", "q[1]", "q[2]", "q[3]"]
    
    # Qubit lines
    for y, lbl in zip(y_lines, labels):
        ax1.plot([0.1, 0.9], [y, y], 'k-', lw=1)
        ax1.text(0.02, y, lbl, va='center', fontsize=9)

    # Layer 1: RY Gates
    for y in y_lines:
        rect_ry = patches.Rectangle((0.15, y-0.04), 0.1, 0.08, facecolor='#64B5F6', edgecolor='k')
        ax1.add_patch(rect_ry)
        ax1.text(0.2, y, "RY", ha='center', va='center', fontsize=7)

    # Layer 2: CNOTs (Ring)
    # q0 -> q1
    ax1.plot([0.35, 0.35], [0.5, 0.4], 'k-', lw=1)
    ax1.plot(0.35, 0.5, 'k.', ms=5)
    ax1.add_patch(patches.Circle((0.35, 0.4), 0.02, facecolor='white', edgecolor='k'))
    
    # q1 -> q2
    ax1.plot([0.45, 0.45], [0.4, 0.3], 'k-', lw=1)
    ax1.plot(0.45, 0.4, 'k.', ms=5)
    ax1.add_patch(patches.Circle((0.45, 0.3), 0.02, facecolor='white', edgecolor='k'))
    
    # q2 -> q3
    ax1.plot([0.55, 0.55], [0.3, 0.2], 'k-', lw=1)
    ax1.plot(0.55, 0.3, 'k.', ms=5)
    ax1.add_patch(patches.Circle((0.55, 0.2), 0.02, facecolor='white', edgecolor='k'))
    
    # q3 -> q0 (Wrap around visually shown as long line)
    ax1.plot([0.65, 0.65], [0.2, 0.5], 'k-', lw=1)
    ax1.plot(0.65, 0.2, 'k.', ms=5) # Control q3
    ax1.add_patch(patches.Circle((0.65, 0.5), 0.02, facecolor='white', edgecolor='k')) # Target q0

    # Layer 3: Final RY
    for y in y_lines:
        rect_ry = patches.Rectangle((0.75, y-0.04), 0.1, 0.08, facecolor='#64B5F6', edgecolor='k')
        ax1.add_patch(rect_ry)
        ax1.text(0.8, y, "RY", ha='center', va='center', fontsize=7)

    # =========================================================================
    # Panel 2: Compiler & QIR
    # =========================================================================
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title("2. 编译层: QIR (LLVM IR)", fontsize=14, pad=10, fontweight='bold')
    ax2.axis('off')
    
    rect2 = patches.Rectangle((0.05, 0.1), 0.9, 0.85, linewidth=1, edgecolor=c_border, facecolor=c_comp)
    ax2.add_patch(rect2)
    
    qir_text = """
%0 = call %Qubit* @get(0)
%1 = call %Qubit* @get(1)
%2 = call %Qubit* @get(2)
%3 = call %Qubit* @get(3)

; Layer 1: RY
call void @ry(double %t0, %0)
call void @ry(double %t1, %1)
call void @ry(double %t2, %2)
call void @ry(double %t3, %3)

; Layer 2: Entanglement (Ring)
call void @cnot(%0, %1) #sensitive=high
call void @cnot(%1, %2) #sensitive=high
call void @cnot(%2, %3) #sensitive=high
call void @cnot(%3, %0) #sensitive=high

; Layer 3: RY
call void @ry(double %t4, %0)
call void @ry(double %t5, %1)
...
"""
    ax2.text(0.1, 0.5, qir_text, fontsize=9, family='monospace', va='center')
    
    # Annotation for Co-PECC
    ax2.annotate("Co-PECC 敏感度标记\n(触发 QOS-DP 动态纠错)", xy=(0.7, 0.3), xytext=(0.5, 0.15),
                 arrowprops=dict(facecolor='red', arrowstyle="->"), fontsize=9, color='red', fontweight='bold')

    # =========================================================================
    # Panel 3: Kernel Mapping (4 Qubits)
    # =========================================================================
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_title("3. 内核层: 拓扑映射 (Grid)", fontsize=14, pad=10, fontweight='bold')
    ax3.axis('off')
    
    rect3 = patches.Rectangle((0.05, 0.1), 0.9, 0.85, linewidth=1, edgecolor=c_border, facecolor=c_kern)
    ax3.add_patch(rect3)
    
    ax3.text(0.5, 0.85, "QPU 2x3 Grid Mapping", ha='center', fontsize=12, fontweight='bold')
    
    # Grid 2x3
    # (0,1) (1,1) (2,1)
    # (0,0) (1,0) (2,0)
    
    grid_coords = {
        (0,0): (0.2, 0.3), (1,0): (0.5, 0.3), (2,0): (0.8, 0.3),
        (0,1): (0.2, 0.6), (1,1): (0.5, 0.6), (2,1): (0.8, 0.6)
    }
    
    # Connections
    lines = [
        ((0,0), (1,0)), ((1,0), (2,0)),
        ((0,1), (1,1)), ((1,1), (2,1)),
        ((0,0), (0,1)), ((1,0), (1,1)), ((2,0), (2,1))
    ]
    
    for start, end in lines:
        p1 = grid_coords[start]
        p2 = grid_coords[end]
        ax3.plot([p1[0], p2[0]], [p1[1], p2[1]], lw=1, color='#CCC')

    # Logical to Physical Mapping
    # q0->(0,1) Q3, q1->(1,1) Q4, q2->(1,0) Q1, q3->(0,0) Q0 (A loop Q0-Q3-Q4-Q1-Q0)
    mapping = {
        "q[0]": (0,1), "q[1]": (1,1), "q[2]": (1,0), "q[3]": (0,0)
    }
    phys_labels = {
        (0,0): "Q0", (1,0): "Q1", (2,0): "Q2",
        (0,1): "Q3", (1,1): "Q4", (2,1): "Q5"
    }
    
    # Highlight used path
    path_edges = [
        ((0,1), (1,1)), # q0-q1
        ((1,1), (1,0)), # q1-q2
        ((1,0), (0,0)), # q2-q3
        ((0,0), (0,1))  # q3-q0
    ]
    for start, end in path_edges:
        p1 = grid_coords[start]
        p2 = grid_coords[end]
        ax3.plot([p1[0], p2[0]], [p1[1], p2[1]], lw=3, color='#4CAF50') # Green path

    for coord, pos in grid_coords.items():
        is_used = coord in mapping.values()
        col = "#81C784" if is_used else "#EEE"
        ec = "black" if is_used else "#CCC"
        c = patches.Circle(pos, 0.06, facecolor=col, edgecolor=ec, zorder=10)
        ax3.add_patch(c)
        lbl = phys_labels[coord]
        # Add logical label if used
        for l_q, p_c in mapping.items():
            if p_c == coord:
                lbl += f"\n({l_q})"
        ax3.text(pos[0], pos[1], lbl, ha='center', va='center', fontsize=9, fontweight='bold' if is_used else 'normal')

    # =========================================================================
    # Panel 4: QEC (Surface Code)
    # =========================================================================
    ax4 = fig.add_subplot(gs[0, 3])
    ax4.set_title("4. 纠错层: 逻辑比特编码", fontsize=14, pad=10, fontweight='bold')
    ax4.axis('off')
    
    rect4 = patches.Rectangle((0.05, 0.1), 0.9, 0.85, linewidth=1, edgecolor=c_border, facecolor=c_qec)
    ax4.add_patch(rect4)
    
    ax4.text(0.5, 0.85, "Surface Code Patch (d=3)", ha='center', fontsize=12, fontweight='bold')
    
    # Draw a single patch representing one logical qubit (symbolic)
    # 3x3 Data grid
    for i in range(3):
        for j in range(3):
            x = 0.25 + i * 0.25
            y = 0.3 + j * 0.2
            c = patches.Circle((x, y), 0.04, facecolor='white', edgecolor='black')
            ax4.add_patch(c)
            # Ancillas
            if i < 2 and j < 2:
                r = patches.Rectangle((x+0.08, y+0.08), 0.08, 0.08, facecolor='black')
                ax4.add_patch(r)
                
    ax4.text(0.5, 0.2, "每个逻辑比特 q[i]\n由 9+ 数据比特编码", ha='center', fontsize=10)
    ax4.text(0.5, 0.1, "实时校正 X/Z 错误", ha='center', fontsize=10, color='red')

    # =========================================================================
    # Panel 5: Hardware Pulse Generation (4 Channels) - Complete Sequence
    # =========================================================================
    ax_hw = fig.add_subplot(gs[1, :])
    ax_hw.set_title("5. 硬件层: 4通道完整脉冲序列 (IQHalDriver -> QPU)", fontsize=14, pad=10, fontweight='bold')
    ax_hw.axis('off')
    
    rect_hw = patches.Rectangle((0.02, 0.05), 0.96, 0.9, linewidth=1, edgecolor=c_border, facecolor=c_hw)
    ax_hw.add_patch(rect_hw)
    
    # Pulse Channels for Q3, Q4, Q1, Q0 (Mapped from q0, q1, q2, q3)
    # Physical Qubits: Q3(q0), Q4(q1), Q1(q2), Q0(q3)
    channels = [
        ("Q3 (q0)", 0.8),
        ("Q4 (q1)", 0.6),
        ("Q1 (q2)", 0.4),
        ("Q0 (q3)", 0.2)
    ]
    
    # Extended time for full sequence:
    # 0-2: RY Layer 1
    # 2-4: CNOT q0-q1
    # 4-6: CNOT q1-q2
    # 6-8: CNOT q2-q3
    # 8-10: CNOT q3-q0
    # 10-12: RY Layer 2
    # 12-14: Readout
    t_end = 15
    t = np.linspace(0, t_end, 1500)
    
    # Define pulse shapes
    def gaussian(t, mu, sigma):
        return np.exp(-(t - mu)**2 / (2 * sigma**2))
        
    def square(t, start, end):
        return np.where((t >= start) & (t <= end), 1.0, 0.0)

    for i, (label, y_base) in enumerate(channels):
        ax_hw.text(0.04, y_base, label, fontsize=11, fontweight='bold', va='center')
        ax_hw.plot([0.1, 0.95], [y_base, y_base], 'k-', lw=1, alpha=0.3)
        
        signal = np.zeros_like(t)
        
        # 1. Layer 1: RY (All channels) t=1
        signal += 0.15 * gaussian(t, 1.0, 0.2) * np.cos(20 * t)
        
        # 2. CNOT Sequence (Ring) - Entanglement involves TWO qubits (Control & Target)
        # CNOT 1: q0(Q3) -> q1(Q4) : t=2.5-3.5
        if "Q3" in label: # Control (Drive Pulse)
            signal += 0.15 * square(t, 2.5, 3.5) * np.sin(10*t)
        if "Q4" in label: # Target (Interaction/Echo Pulse)
            signal += 0.08 * square(t, 2.5, 3.5) * np.sin(15*t)
            
        # CNOT 2: q1(Q4) -> q2(Q1) : t=4.5-5.5
        if "Q4" in label: # Control
            signal += 0.15 * square(t, 4.5, 5.5) * np.sin(10*t)
        if "Q1" in label: # Target
            signal += 0.08 * square(t, 4.5, 5.5) * np.sin(15*t)
            
        # CNOT 3: q2(Q1) -> q3(Q0) : t=6.5-7.5
        if "Q1" in label: # Control
            signal += 0.15 * square(t, 6.5, 7.5) * np.sin(10*t)
        if "Q0" in label: # Target
            signal += 0.08 * square(t, 6.5, 7.5) * np.sin(15*t)
            
        # CNOT 4: q3(Q0) -> q0(Q3) : t=8.5-9.5
        if "Q0" in label: # Control
            signal += 0.15 * square(t, 8.5, 9.5) * np.sin(10*t)
        if "Q3" in label: # Target
            signal += 0.08 * square(t, 8.5, 9.5) * np.sin(15*t)
            
        # 3. Layer 2: RY (All channels) t=11
        signal += 0.15 * gaussian(t, 11.0, 0.2) * np.cos(20 * t)
        
        # 4. Readout: t=13
        signal += 0.10 * square(t, 12.5, 14.0) # Flat readout pulse
        
        # Plot signal
        ax_hw.plot(t/16 + 0.1, signal + y_base, 'b-', lw=1)
        
    # Annotations
    y_top = 0.92
    ax_hw.text(0.16, y_top, "Layer 1: RY", color='blue', fontsize=9, ha='center')
    ax_hw.text(0.28, y_top, "CNOT 1\n(q0->q1)", color='black', fontsize=8, ha='center')
    ax_hw.text(0.40, y_top, "CNOT 2\n(q1->q2)", color='black', fontsize=8, ha='center')
    ax_hw.text(0.52, y_top, "CNOT 3\n(q2->q3)", color='black', fontsize=8, ha='center')
    ax_hw.text(0.64, y_top, "CNOT 4\n(q3->q0)", color='black', fontsize=8, ha='center')
    ax_hw.text(0.78, y_top, "Layer 2: RY", color='blue', fontsize=9, ha='center')
    ax_hw.text(0.90, y_top, "Readout", color='purple', fontsize=9, ha='center')

    plt.tight_layout()
    plt.savefig('vqe_workflow_full.png', dpi=300)
    print("Generated vqe_workflow_full.png")

if __name__ == "__main__":
    draw_vqe_workflow()