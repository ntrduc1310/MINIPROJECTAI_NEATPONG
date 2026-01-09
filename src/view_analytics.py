"""
View Analytics - Script đơn giản để xem training analytics
Chạy: python view_analytics.py
"""
import csv
import os
from pathlib import Path


def find_latest_log():
    """Tìm file log mới nhất"""
    log_dir = Path("logs")
    if not log_dir.exists():
        print(" Không tìm thấy thư mục logs!")
        return None, None
    
    # Tìm file generation và genome mới nhất
    gen_files = list(log_dir.glob("generation_*.csv"))
    genome_files = list(log_dir.glob("genome_*.csv"))
    
    if not gen_files:
        print(" Không tìm thấy file log!")
        return None, None
    
    latest_gen = max(gen_files, key=lambda f: f.stat().st_mtime)
    latest_genome = max(genome_files, key=lambda f: f.stat().st_mtime) if genome_files else None
    
    return latest_gen, latest_genome


def print_generation_summary(file_path):
    """In tóm tắt training theo generation"""
    print("\n" + "="*70)
    print(" TRAINING SUMMARY - GENERATION STATS")
    print("="*70)
    print(f"File: {file_path.name}\n")
    
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        if not rows:
            print(" Không có dữ liệu!")
            return
        
        # Thống kê tổng quan
        total_gens = len(rows)
        first_gen = rows[0]
        last_gen = rows[-1]
        
        print(f" Tổng số Generations: {total_gens}")
        print(f"  Thời gian: {first_gen.get('Timestamp', 'N/A').split('T')[0]} → {last_gen.get('Timestamp', 'N/A').split('T')[0]}")
        print()
        
        # Fitness progression
        print(" FITNESS PROGRESSION:")
        print(f"   Generation 1:   Best={float(first_gen['BestFitness']):.2f}, Avg={float(first_gen['AvgFitness']):.2f}")
        print(f"   Generation {total_gens}: Best={float(last_gen['BestFitness']):.2f}, Avg={float(last_gen['AvgFitness']):.2f}")
        
        # Tìm best fitness ever
        best_fitness = max(float(row['BestFitness']) for row in rows)
        best_gen = next(i+1 for i, row in enumerate(rows) if float(row['BestFitness']) == best_fitness)
        print(f"    Best Ever:    {best_fitness:.2f} (Generation {best_gen})")
        print()
        
        # Species stats
        print("🧬 SPECIES DIVERSITY:")
        avg_species = sum(float(row['SpeciesCount']) for row in rows) / len(rows)
        print(f"   Average Species: {avg_species:.1f}")
        print(f"   Current Species: {last_gen['SpeciesCount']}")
        print()
        
        # Recent performance (last 10 gens)
        print(" RECENT PERFORMANCE (Last 10 Generations):")
        print("-" * 70)
        print(f"{'Gen':<6} {'Best':>10} {'Avg':>10} {'Min':>10} {'StdDev':>10} {'Species':>10}")
        print("-" * 70)
        
        recent = rows[-10:] if len(rows) >= 10 else rows
        for i, row in enumerate(recent):
            gen = int(row['Generation'])
            best = float(row['BestFitness'])
            avg = float(row['AvgFitness'])
            min_fit = float(row['MinFitness'])
            std = float(row['StdDev'])
            species = row['SpeciesCount']
            
            print(f"{gen:<6} {best:>10.2f} {avg:>10.2f} {min_fit:>10.2f} {std:>10.2f} {species:>10}")
        
        print("="*70)


def print_genome_summary(file_path):
    """In tóm tắt genome complexity"""
    print("\n" + "="*70)
    print(" GENOME COMPLEXITY ANALYSIS")
    print("="*70)
    print(f"File: {file_path.name}\n")
    
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        if not rows:
            print(" Không có dữ liệu!")
            return
        
        # Phân tích genome của generation cuối
        last_gen = max(int(row['Generation']) for row in rows)
        last_gen_genomes = [row for row in rows if int(row['Generation']) == last_gen]
        
        print(f" Generation {last_gen} - Tổng số genomes: {len(last_gen_genomes)}\n")
        
        # Stats
        fitnesses = [float(row['Fitness']) for row in last_gen_genomes]
        nodes = [int(row['Nodes']) for row in last_gen_genomes]
        connections = [int(row['Connections']) for row in last_gen_genomes]
        
        print(" FITNESS DISTRIBUTION:")
        print(f"   Max:     {max(fitnesses):.2f}")
        print(f"   Average: {sum(fitnesses)/len(fitnesses):.2f}")
        print(f"   Min:     {min(fitnesses):.2f}")
        print()
        
        print(" NETWORK COMPLEXITY:")
        print(f"   Nodes:       {sum(nodes)/len(nodes):.1f} (avg) | Range: {min(nodes)}-{max(nodes)}")
        print(f"   Connections: {sum(connections)/len(connections):.1f} (avg) | Range: {min(connections)}-{max(connections)}")
        print()
        
        # Top 5 genomes
        print(" TOP 5 GENOMES:")
        print("-" * 70)
        print(f"{'Rank':<6} {'ID':<10} {'Fitness':>10} {'Nodes':>10} {'Connections':>10}")
        print("-" * 70)
        
        sorted_genomes = sorted(last_gen_genomes, key=lambda x: float(x['Fitness']), reverse=True)
        for i, genome in enumerate(sorted_genomes[:5], 1):
            print(f"{i:<6} {genome['GenomeID']:<10} {float(genome['Fitness']):>10.2f} "
                  f"{genome['Nodes']:>10} {genome['Connections']:>10}")
        
        print("="*70)


def main():
    """Main function"""
    print("\n NEAT PONG - TRAINING ANALYTICS VIEWER")
    
    # Tìm file log mới nhất
    gen_file, genome_file = find_latest_log()
    
    if not gen_file:
        return
    
    # Hiển thị generation stats
    print_generation_summary(gen_file)
    
    # Hiển thị genome stats nếu có
    if genome_file:
        print_genome_summary(genome_file)
    
    print("\n Hoàn tất! Để xem biểu đồ chi tiết, chạy: python visualize_full_report.py\n")


if __name__ == "__main__":
    main()
