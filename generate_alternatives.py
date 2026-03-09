import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import numpy as np

# Set Chinese font
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_alternatives():
    fig = plt.figure(figsize=(20, 16), constrained_layout=True)
    gs = GridSpec(2, 2, figure=fig, height_ratios=[1, 1], width_ratios=[1.2, 0.8])
    
    # Colors
    c_neutral = "#E8F5E9" # Green 50
    c_ion     = "#E3F2FD" # Blue 50
    c_pulse   = "#FFF3E0" # Orange 50
    c_border  = "#333333"

    # =========================================================================
    # Panel 1: Neutral Atom Architecture (Rydberg Blockade)
    # =========================================================================
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title("1. 中性原子 (Neutral Atoms): 阵列与里德堡阻塞", fontsize=14, pad=10, fontweight='bold')
    ax1.axis('off')
    
    # Background
    rect1 = patches.Rectangle((0.05, 0.05), 0.9, 0.9, linewidth=1, edgecolor=c_border, facecolor=c_neutral)
    ax1.add_patch(rect1)
    
    # Atom Grid (4x4)
    # Tweezer Array
    for i in range(4):
        for j in range(4):
            x = 0.2 + i * 0.15
            y = 0.2 + j * 0.15
            
            # Tweezer trap (small potential well visual)
            trap = patches.Circle((x, y), 0.04, facecolor='none', edgecolor='#999', linestyle='--')
            ax1.add_patch(trap)
            
            # Atom
            atom_color = '#66BB6A' # Green
            
            # Highlight Control/Target for CZ Gate
            is_control = (i==1 and j==2)
            is_target  = (i==2 and j==2)
            
            if is_control:
                atom_color = '#FF7043' # Orange Control
                # Rydberg Blockade Radius
                blockade = patches.Circle((x, y), 0.22, facecolor='red', alpha=0.1, edgecolor='red', linestyle='--')
                ax1.add_patch(blockade)
                ax1.text(x, y+0.25, "Rydberg Blockade (R_b)", ha='center', color='red', fontsize=10)
                ax1.text(x, y, "Control", ha='center', va='center', fontsize=9, fontweight='bold', color='white')
            elif is_target:
                atom_color = '#42A5F5' # Blue Target
                ax1.text(x, y, "Target", ha='center', va='center', fontsize=9, fontweight='bold', color='white')
            else:
                ax1.text(x, y, f"q{i*4+j}", ha='center', va='center', fontsize=8, color='white')

            atom = patches.Circle((x, y), 0.03, facecolor=atom_color, edgecolor='black')
            ax1.add_patch(atom)
            
    # Labels
    ax1.text(0.1, 0.85, "光镊阵列 (Tweezer Array)", fontsize=12, fontweight='bold')
    ax1.text(0.1, 0.80, "- 全同性原子 (Rb87)", fontsize=10)
    ax1.text(0.1, 0.75, "- 动态重构拓扑", fontsize=10)
    ax1.text(0.7, 0.85, "CZ Gate Mechanism:", fontsize=11, fontweight='bold')
    ax1.text(0.7, 0.80, "When Control is excited to |r>,\nTarget cannot be excited due to\nEnergy Shift (Blockade).", fontsize=9, ha='left')

    # =========================================================================
    # Panel 2: Neutral Atom Pulse Sequence
    # =========================================================================
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title("脉冲序列: Global & Local Lasers", fontsize=12, pad=10)
    ax2.axis('off')
    
    rect2 = patches.Rectangle((0.05, 0.05), 0.9, 0.9, linewidth=1, edgecolor=c_border, facecolor=c_pulse)
    ax2.add_patch(rect2)
    
    t = np.linspace(0, 10, 500)
    
    # Pulse 1: Global Rabi (Omega) - Drives all to superposition
    y_global = 0.7
    ax2.text(0.08, y_global, "Global \u03A9 (Rabi)", fontsize=10, fontweight='bold')
    pulse_global = 0.2 * np.exp(-(t-2)**2/0.5) + 0.2 * np.exp(-(t-8)**2/0.5)
    ax2.plot(t/12 + 0.1, pulse_global + y_global, 'b-')
    ax2.plot([0.1, 0.9], [y_global, y_global], 'k-', alpha=0.3)
    
    # Pulse 2: Local Detuning (Delta) - Addresses specific atoms
    y_local = 0.4
    ax2.text(0.08, y_local, "Local \u0394 (Detuning)\n(Target Atom)", fontsize=10, fontweight='bold')
    pulse_local = 0.25 * (np.abs(t-5) < 1.5).astype(float) # Square pulse
    ax2.plot(t/12 + 0.1, pulse_local + y_local, 'r-')
    ax2.plot([0.1, 0.9], [y_local, y_local], 'k-', alpha=0.3)
    
    ax2.text(0.5, 0.2, "CZ Gate Operation:\n1. \u03C0-pulse on Control (|g>->|r>)\n2. 2\u03C0-pulse on Target (blocked if C=|r>)\n3. \u03C0-pulse on Control (|r>->|g>)", 
             ha='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.8))

    # =========================================================================
    # Panel 3: Ion Trap Architecture (Linear Chain)
    # =========================================================================
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_title("2. 离子阱 (Ion Trap): 线性链与声子总线", fontsize=14, pad=10, fontweight='bold')
    ax3.axis('off')
    
    rect3 = patches.Rectangle((0.05, 0.05), 0.9, 0.9, linewidth=1, edgecolor=c_border, facecolor=c_ion)
    ax3.add_patch(rect3)
    
    # Linear Trap Electrodes (Top/Bottom)
    ax3.plot([0.1, 0.9], [0.7, 0.7], 'k-', lw=3, color='#555') # Top electrode
    ax3.plot([0.1, 0.9], [0.3, 0.3], 'k-', lw=3, color='#555') # Bottom electrode
    
    # Ions
    num_ions = 5
    for i in range(num_ions):
        x = 0.2 + i * 0.15
        y = 0.5
        
        # Ion
        ion_color = '#29B6F6' # Light Blue
        if i == 1: ion_color = '#EF5350' # Red (Active 1)
        if i == 3: ion_color = '#EF5350' # Red (Active 2)
        
        ion = patches.Circle((x, y), 0.04, facecolor=ion_color, edgecolor='black', zorder=10)
        ax3.add_patch(ion)
        ax3.text(x, y-0.08, f"Ion {i}", ha='center', fontsize=9)
        
        # Laser Beams targeting ions
        if i in [1, 3]:
            # Draw laser beam
            ax3.arrow(x-0.05, 0.85, 0.05, -0.3, head_width=0.02, head_length=0.03, fc='#E040FB', ec='#E040FB', width=0.005)
            ax3.text(x, 0.9, "Raman\nBeams", ha='center', fontsize=8, color='#E040FB')

    # Phonon Mode (Wavy line)
    x_vals = np.linspace(0.2, 0.2 + (num_ions-1)*0.15, 200)
    y_vals = 0.5 + 0.02 * np.sin(20 * x_vals)
    ax3.plot(x_vals, y_vals, 'g--', lw=1, alpha=0.6, zorder=5)
    ax3.text(0.5, 0.55, "Shared Phonon Bus (Motional Mode)", ha='center', color='green', fontsize=10, fontweight='bold', backgroundcolor='white')

    ax3.text(0.1, 0.2, "优势 (Pros):", fontsize=10, fontweight='bold')
    ax3.text(0.1, 0.15, "- 全连接 (All-to-All Connectivity)", fontsize=9)
    ax3.text(0.1, 0.1, "- 长相干时间 (Seconds to Minutes)", fontsize=9)

    # =========================================================================
    # Panel 4: Ion Trap Pulse Sequence (MS Gate)
    # =========================================================================
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_title("脉冲序列: Mølmer-Sørensen (MS) Gate", fontsize=12, pad=10)
    ax4.axis('off')
    
    rect4 = patches.Rectangle((0.05, 0.05), 0.9, 0.9, linewidth=1, edgecolor=c_border, facecolor=c_pulse)
    ax4.add_patch(rect4)
    
    # MS Gate Pulses (Bichromatic)
    # Red sideband + Blue sideband
    
    t = np.linspace(0, 10, 500)
    
    # Ion 1 Laser
    y_ion1 = 0.7
    ax4.text(0.08, y_ion1, "Ion 1 (Raman)", fontsize=10, fontweight='bold')
    # Bichromatic pulse: carrier modulated by beat note
    pulse_ion1 = 0.25 * np.sin(5*t) * np.sin(50*t) * (t>2) * (t<8) 
    # Use envelope for visual clarity
    envelope = 0.25 * (t>2) * (t<8)
    ax4.plot(t/12 + 0.1, envelope + y_ion1, 'm-', alpha=0.8)
    ax4.plot([0.1, 0.9], [y_ion1, y_ion1], 'k-', alpha=0.3)
    
    # Ion 3 Laser
    y_ion3 = 0.4
    ax4.text(0.08, y_ion3, "Ion 3 (Raman)", fontsize=10, fontweight='bold')
    pulse_ion3 = 0.25 * np.sin(5*t) * np.sin(50*t) * (t>2) * (t<8)
    ax4.plot(t/12 + 0.1, envelope + y_ion3, 'm-', alpha=0.8)
    ax4.plot([0.1, 0.9], [y_ion3, y_ion3], 'k-', alpha=0.3)
    
    ax4.text(0.5, 0.2, "MS Gate Operation:\nSimultaneous irradiation of two ions\nwith bichromatic beams creates\nentanglement via phonon bus.", 
             ha='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig('alternatives_workflow.png', dpi=300)
    print("Generated alternatives_workflow.png")

if __name__ == "__main__":
    draw_alternatives()
