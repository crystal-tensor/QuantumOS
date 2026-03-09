import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np

# Set Chinese font
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def generate_surface_code_gif():
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # ---------------------------------------------------------
    # Define Layout (Rotated Surface Code d=3)
    # ---------------------------------------------------------
    # Data Qubits (Circles) at integer coordinates
    data_qubits = []
    for x in range(5):
        for y in range(5):
            if (x + y) % 2 == 0: # Checkerboard pattern for Data
                # Actually, standard rotated code usually puts Data on edges
                # Let's use a simplified model for visualization:
                # Data Qubits at vertices (0,0) to (2,2) for a small patch
                pass

    # Simplified 3x3 Data Grid (9 Data Qubits)
    # Data at (x,y) for x,y in 0,1,2
    dq_pos = [(x, y) for x in range(3) for y in range(3)]
    
    # Z-Stabilizers (Check Parity of Z on 4 neighbors) -> Detect X Errors
    # Placed at center of plaquettes
    # (0.5, 0.5), (0.5, 1.5), (1.5, 0.5), (1.5, 1.5)
    z_stab_pos = [(0.5, 0.5), (0.5, 1.5), (1.5, 0.5), (1.5, 1.5)]
    
    # X-Stabilizers (Check Parity of X on 4 neighbors) -> Detect Z Errors
    # We will omit X-stabilizers for clarity in this X-error demo, 
    # or place them at vertices if using a different lattice. 
    # For rotated code, let's just show the Z-plaquettes relevant to X-error.
    
    # ---------------------------------------------------------
    # Drawing Elements
    # ---------------------------------------------------------
    
    # Background Grid
    for x in range(3):
        ax.plot([x, x], [0, 2], 'k-', lw=1, color='#ddd', zorder=0)
        ax.plot([0, 2], [x, x], 'k-', lw=1, color='#ddd', zorder=0)

    # Title
    title_text = ax.text(1, 4.2, "", ha='center', fontsize=16, fontweight='bold')
    desc_text = ax.text(1, 3.8, "", ha='center', fontsize=12, color='#555')

    # Data Qubits (Circles)
    dq_patches = {}
    for (x, y) in dq_pos:
        circle = patches.Circle((x, y), 0.15, facecolor='white', edgecolor='black', lw=2, zorder=2)
        ax.add_patch(circle)
        dq_patches[(x, y)] = circle
        ax.text(x, y-0.3, f"D{x}{y}", ha='center', fontsize=8, color='#888')

    # Z-Ancilla Qubits (Squares)
    zq_patches = {}
    for (x, y) in z_stab_pos:
        rect = patches.Rectangle((x-0.1, y-0.1), 0.2, 0.2, facecolor='#E1BEE7', edgecolor='purple', lw=2, zorder=2) # Purple
        ax.add_patch(rect)
        zq_patches[(x, y)] = rect
        # Connections
        # Connect Ancilla to its 4 data neighbors
        neighbors = [
            (int(x-0.5), int(y-0.5)), (int(x-0.5), int(y+0.5)),
            (int(x+0.5), int(y-0.5)), (int(x+0.5), int(y+0.5))
        ]
        for nx, ny in neighbors:
            if (nx, ny) in dq_patches:
                ax.plot([x, nx], [y, ny], '-', color='#E1BEE7', lw=2, zorder=1)

    # ---------------------------------------------------------
    # Animation Logic
    # ---------------------------------------------------------
    # Scenario: X Error on D(1,1) (Center)
    # Detected by all 4 surrounding Z-stabilizers
    
    # Steps:
    # 0-9: Idle
    # 10-19: Error Injection (Red Flash on D(1,1))
    # 20-29: Syndrome Measurement (Ancillas Flash Red)
    # 30-39: Decoding (Highlight edges/match)
    # 40-49: Correction (Green Flash on D(1,1))
    # 50-59: Recovered

    def update(frame):
        step = frame // 10
        sub_step = frame % 10
        
        # Reset colors
        for c in dq_patches.values(): c.set_facecolor('white')
        for r in zq_patches.values(): r.set_facecolor('#E1BEE7') # Light Purple
        
        target_q = (1, 1) # The center qubit
        affected_ancillas = z_stab_pos # All 4 surround (1,1)

        if step == 0:
            title_text.set_text("Step 1: 初始状态 (Idle)")
            desc_text.set_text("逻辑比特处于基态 |00...0>")
            
        elif step == 1:
            title_text.set_text("Step 2: 错误注入 (Error Injection)")
            desc_text.set_text("环境噪声导致 D11 发生 X-Flip (比特翻转)")
            # Flash Red
            if sub_step % 2 == 0:
                dq_patches[target_q].set_facecolor('#FF5252') # Red
            else:
                dq_patches[target_q].set_facecolor('white')
                
        elif step == 2:
            title_text.set_text("Step 3: 综合征测量 (Syndrome Measurement)")
            desc_text.set_text("相邻的 Z-Ancilla 测量到奇偶性变化 (-1)")
            # Keep error red
            dq_patches[target_q].set_facecolor('#FFCDD2') # Light Red
            # Flash Ancillas
            for pos in affected_ancillas:
                if sub_step > 2:
                    zq_patches[pos].set_facecolor('#AB47BC') # Dark Purple (Active)
                    
        elif step == 3:
            title_text.set_text("Step 4: 解码与匹配 (Decoding)")
            desc_text.set_text("MWPM 算法定位错误源头 -> D11")
            # Keep error and ancillas
            dq_patches[target_q].set_facecolor('#FFCDD2')
            for pos in affected_ancillas:
                zq_patches[pos].set_facecolor('#AB47BC')
            
            # Draw imaginary matching lines (optional, maybe just text is enough)
            
        elif step == 4:
            title_text.set_text("Step 5: 纠错操作 (Correction)")
            desc_text.set_text("施加 X 门翻转回原始状态")
            # Flash Green
            if sub_step % 2 == 0:
                dq_patches[target_q].set_facecolor('#69F0AE') # Green
            else:
                dq_patches[target_q].set_facecolor('#FFCDD2')

        elif step == 5:
            title_text.set_text("Step 6: 恢复完成 (Recovered)")
            desc_text.set_text("系统回到逻辑基态")
            dq_patches[target_q].set_facecolor('white')

    ani = animation.FuncAnimation(fig, update, frames=60, interval=200)
    ani.save('surface_code_qec.gif', writer='pillow', dpi=100)
    print("Generated surface_code_qec.gif")

if __name__ == "__main__":
    generate_surface_code_gif()