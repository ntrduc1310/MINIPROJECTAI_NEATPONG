import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import seaborn as sns

# Cấu hình giao diện đẹp
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 10})


def get_latest_log_files():
    # Tìm file generation log mới nhất
    gen_files = glob.glob('logs/generation_*.csv')
    if not gen_files: return None, None
    latest_gen = max(gen_files, key=os.path.getctime)

    # Tìm file genome log tương ứng (cùng timestamp)
    # Giả định timestamp giống nhau: generation_2025... và genome_2025...
    timestamp = latest_gen.split('_')[-1].replace('.csv', '')
    genome_files = glob.glob(f'logs/genome_*{timestamp}*.csv')
    latest_genome = genome_files[0] if genome_files else None

    return latest_gen, latest_genome


def plot_full_dashboard():
    gen_file, genome_file = get_latest_log_files()
    if not gen_file:
        print("Không tìm thấy file log!")
        return

    print(f"Đang xử lý: {gen_file}")
    df_gen = pd.read_csv(gen_file)

    df_genome = None
    if genome_file:
        print(f"Đang xử lý: {genome_file}")
        df_genome = pd.read_csv(genome_file)

    # Tạo khung hình lớn chứa 4 biểu đồ con
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Kết Quả Thực Nghiệm NEAT-Pong AI', fontsize=16, fontweight='bold')

    # --- BIỂU ĐỒ 1: SỰ HỘI TỤ (Fitness) ---
    ax1 = axs[0, 0]
    ax1.plot(df_gen['Generation'], df_gen['BestFitness'], 'r-', label='Best Fitness')
    ax1.plot(df_gen['Generation'], df_gen['AvgFitness'], 'b--', label='Avg Fitness', alpha=0.7)
    ax1.fill_between(df_gen['Generation'],
                     df_gen['AvgFitness'] - df_gen['StdDev'],
                     df_gen['AvgFitness'] + df_gen['StdDev'],
                     color='blue', alpha=0.1, label='Std Dev')
    ax1.set_title('Quá trình Hội tụ Fitness')
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Fitness Score')
    ax1.legend()

    # --- BIỂU ĐỒ 2: ĐA DẠNG LOÀI (Speciation) ---
    ax2 = axs[0, 1]
    ax2.plot(df_gen['Generation'], df_gen['SpeciesCount'], 'g-o', linewidth=2)
    ax2.set_title('Sự Đa dạng Quần thể (Species Count)')
    ax2.set_xlabel('Generation')
    ax2.set_ylabel('Số lượng Loài')
    ax2.grid(True, linestyle='--')

    # --- BIỂU ĐỒ 3: TIẾN HÓA CẤU TRÚC (Topology) ---
    ax3 = axs[1, 0]
    if df_genome is not None:
        # Tính trung bình số nodes/connections mỗi thế hệ
        avg_topology = df_genome.groupby('Generation')[['Nodes', 'Connections']].mean()
        ax3.plot(avg_topology.index, avg_topology['Nodes'], 'purple', label='Avg Nodes')
        ax3.plot(avg_topology.index, avg_topology['Connections'], 'orange', label='Avg Connections')
        ax3.set_title('Sự Phức tạp hóa Mạng Nơ-ron (Complexification)')
        ax3.set_xlabel('Generation')
        ax3.set_ylabel('Số lượng')
        ax3.legend()
    else:
        ax3.text(0.5, 0.5, 'Thiếu file genome_*.csv', ha='center')

    # --- BIỂU ĐỒ 4: TỐC ĐỘ HUẤN LUYỆN ---
    ax4 = axs[1, 1]
    ax4.bar(df_gen['Generation'], df_gen['Duration(s)'], color='teal', alpha=0.6)
    ax4.plot(df_gen['Generation'], df_gen['Duration(s)'].rolling(window=5).mean(), 'r-', label='Moving Avg')
    ax4.set_title('Thời gian Huấn luyện mỗi Thế hệ')
    ax4.set_xlabel('Generation')
    ax4.set_ylabel('Thời gian (giây)')
    ax4.legend()

    # Lưu và hiển thị
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)  # Chừa chỗ cho Title chính
    
    # Lưu với chất lượng cao cho báo cáo
    output_path = 'full_report_charts.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Đã lưu biểu đồ: {output_path}")
    print(f"   - Số generations: {len(df_gen)}")
    print(f"   - Best Fitness cuối: {df_gen['BestFitness'].iloc[-1]:.2f}")
    print(f"   - Avg Fitness cuối: {df_gen['AvgFitness'].iloc[-1]:.2f}")
    print(f"   - Training time trung bình: {df_gen['Duration(s)'].mean():.3f}s/gen")
    plt.show()


if __name__ == "__main__":
    plot_full_dashboard()