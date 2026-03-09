import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib

# Set Chinese font
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_mlfq_diagram():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Define styles
    box_style = dict(boxstyle="round,pad=0.5", fc="#e1f5fe", ec="#0277bd", lw=2)
    queue_style = dict(boxstyle="round,pad=0.5", fc="#fff9c4", ec="#fbc02d", lw=2)
    state_style = dict(boxstyle="circle,pad=0.5", fc="#e0f2f1", ec="#00695c", lw=2)
    
    # Draw States
    ax.text(1, 7, "新任务", ha="center", va="center", size=12, bbox=state_style)
    
    # Queues
    ax.text(4, 7, "队列 1\n(高优先级)\n时间片 = 10ms", ha="center", va="center", size=10, bbox=queue_style)
    ax.text(4, 5, "队列 2\n(中优先级)\n时间片 = 20ms", ha="center", va="center", size=10, bbox=queue_style)
    ax.text(4, 3, "队列 3\n(低优先级)\n时间片 = 40ms", ha="center", va="center", size=10, bbox=queue_style)
    
    ax.text(8, 5, "运行中\n(QPU)", ha="center", va="center", size=12, bbox=dict(boxstyle="round,pad=0.8", fc="#ffcdd2", ec="#c62828", lw=2))
    
    ax.text(11, 5, "已终止", ha="center", va="center", size=12, bbox=state_style)
    
    ax.text(4, 1, "阻塞\n(I/O 等待 / 混合任务)", ha="center", va="center", size=12, bbox=dict(boxstyle="round,pad=0.5", fc="#e1bee7", ec="#6a1b9a", lw=2))
    
    # Arrows
    arrow_props = dict(arrowstyle="->", color="black", lw=1.5, shrinkA=5, shrinkB=5)
    curved_arrow = dict(arrowstyle="->", color="black", lw=1.5, connectionstyle="arc3,rad=0.2", shrinkA=5, shrinkB=5)
    
    # New -> Q1
    ax.annotate("准入", xy=(2.5, 7), xytext=(1.5, 7), arrowprops=arrow_props, ha="center")
    ax.annotate("", xy=(3, 7), xytext=(2.5, 7), arrowprops=arrow_props)

    # Q1 -> Running
    ax.annotate("调度", xy=(7.2, 5.5), xytext=(5.2, 7), arrowprops=arrow_props, ha="center")
    
    # Q2 -> Running
    ax.annotate("调度", xy=(7.2, 5), xytext=(5.2, 5), arrowprops=arrow_props, ha="center")
    
    # Q3 -> Running
    ax.annotate("调度", xy=(7.2, 4.5), xytext=(5.2, 3), arrowprops=arrow_props, ha="center")
    
    # Running -> Terminated
    ax.annotate("退出", xy=(10.5, 5), xytext=(8.8, 5), arrowprops=arrow_props, ha="center")
    
    # Running -> Q2 (Downgrade)
    ax.annotate("时间片耗尽", xy=(5.2, 5.2), xytext=(7.5, 5.5), 
                arrowprops=dict(arrowstyle="->", color="red", lw=1.5, connectionstyle="arc3,rad=-0.2"), ha="center", color="red")

    # Running -> Q3 (Downgrade)
    ax.annotate("时间片耗尽", xy=(5.2, 3.2), xytext=(7.5, 4.5), 
                arrowprops=dict(arrowstyle="->", color="red", lw=1.5, connectionstyle="arc3,rad=-0.2"), ha="center", color="red")
    
    # Running -> Blocked
    ax.annotate("I/O 请求", xy=(5.2, 1.5), xytext=(8, 4.2), arrowprops=arrow_props, ha="center")
    
    # Blocked -> Q1 (Boost)
    ax.annotate("I/O 完成\n(优先级提升)", xy=(3, 6.5), xytext=(3, 1.5), 
                arrowprops=dict(arrowstyle="->", color="green", lw=1.5, connectionstyle="arc3,rad=-0.3"), ha="center", color="green")

    plt.title("图 2：多级反馈队列 (MLFQ) 调度器状态流转图", fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig('patent_fig2_mlfq.png', dpi=300)
    print("Generated patent_fig2_mlfq.png")

def draw_qos_dp_sequence():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Lifelines
    actors = ["用户 (SDK)", "编译层\n(Compiler)", "QOS 内核\n(调度/资源)", "纠错层\n(QEC)", "Q-HAL 驱动\n(QOS-DP)", "量子硬件\n(QPU)"]
    x_pos = [1, 3.5, 6, 8.5, 11, 13.5]
    colors = ["#bbdefb", "#e1bee7", "#c8e6c9", "#ffccbc", "#fff9c4", "#ffab91"]
    
    for x, actor, color in zip(x_pos, actors, colors):
        ax.text(x, 11.5, actor, ha="center", va="center", size=11, bbox=dict(boxstyle="round,pad=0.5", fc=color, ec="black"))
        ax.plot([x, x], [0.5, 11], color="black", linestyle="--", lw=1)

    # Sequence Actions
    y = 10.5
    step = 0.8
    
    def add_msg(src_idx, dst_idx, msg, y_pos, color="black", style="->", linestyle="-"):
        x_start = x_pos[src_idx]
        x_end = x_pos[dst_idx]
        ax.annotate(msg, xy=(x_end, y_pos), xytext=(x_start, y_pos),
                    arrowprops=dict(arrowstyle=style, color=color, lw=1.5, linestyle=linestyle),
                    ha="center", va="bottom", fontsize=10)

    # 0. System Init
    add_msg(2, 4, "1. 系统初始化: 加载驱动", y)
    y -= step

    # 1. User Submit
    add_msg(0, 1, "2. 提交源代码 (Python/QASM)", y, color="blue")
    y -= step
    
    # 2. Compile
    ax.text(x_pos[1] + 0.2, y, "[语法分析 & 优化]", ha="left", va="center", fontsize=9, style="italic", color="purple")
    y -= step
    add_msg(1, 2, "3. 提交 QIR 中间表示", y, color="purple")
    y -= step
    
    # 3. Kernel Schedule
    ax.text(x_pos[2] + 0.2, y, "[优先级调度 & 映射]", ha="left", va="center", fontsize=9, style="italic", color="green")
    y -= step
    
    # 4. Dispatch
    add_msg(2, 4, "4. 下发物理指令", y)
    y -= step

    # 5. Driver Exec
    add_msg(4, 5, "5. 发送微波脉冲 (DAC)", y, color="red")
    y -= step

    # 6. QEC Loop
    add_msg(5, 3, "6. 错误综合征测量", y, color="red", linestyle="--")
    y -= 0.5
    add_msg(3, 5, "7. 实时纠错反馈", y, color="red")
    y -= step

    # 7. Result
    add_msg(5, 4, "8. 读取最终态 (ADC)", y, linestyle="--", color="red")
    y -= step

    # 8. Return
    add_msg(4, 2, "9. 返回执行结果", y, linestyle="--")
    y -= step

    # 9. Final Return
    add_msg(2, 0, "10. 返回最终数据", y, linestyle="--", color="blue")

    plt.title("图 3：QOS-DP 驱动加载与执行时序图", fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig('patent_fig3_qos_dp.png', dpi=300)
    print("Generated patent_fig3_qos_dp.png")

if __name__ == "__main__":
    draw_mlfq_diagram()
    draw_qos_dp_sequence()
