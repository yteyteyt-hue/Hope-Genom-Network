#!/usr/bin/env python3
"""
benchmark.py - Automated Benchmarking Suite for Hope Genome

Generates all tables and figures referenced in the supplementary material.
Designed to be fully reproducible across different hardware platforms.

Usage:
    python benchmark.py --test all
    python benchmark.py --test integrity
    python benchmark.py --test collective
    python benchmark.py --test memory
    python benchmark.py --generate-plots
"""

import argparse
import asyncio
import json
import os
import sys
import time
import gc
from pathlib import Path
from typing import Dict, List, Any
from statistics import mean, stdev
from collections import deque
import timeit

sys.path.insert(0, os.path.dirname(__file__))

# Assuming hope_genome.py is in the same directory
from hope_genome import (
    GenomeBuilder,
    HopeGenome,
    HopeGenomeRuntime,
    DecisionContext,
    RiskLevel,
    EthicsDecision,
    EmotionalState,
    PresenceLayer,
    CollectiveIntelligence,
    ResonanceNode
)

# Optional: plotting libraries
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False
    print("Warning: matplotlib/seaborn not available. Plots will be skipped.")

# Configure output
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)


class BenchmarkSuite:
    """Complete benchmarking suite for Hope Genome."""
    
    def __init__(self):
        self.results = {}
    
    def run_all(self):
        """Run all benchmarks."""
        print("\n" + "="*70)
        print("HOPE GENOME - COMPREHENSIVE BENCHMARK SUITE")
        print("="*70 + "\n")
        
        self.benchmark_integrity_latency()
        self.benchmark_hash_algorithms()
        asyncio.run(self.benchmark_collective_scaling())
        self.benchmark_presence_memory()
        self.benchmark_high_load()
        
        # Save results
        self.save_results()
        
        print("\n" + "="*70)
        print("ALL BENCHMARKS COMPLETE")
        print("="*70 + "\n")
        print(f"Results saved to: {RESULTS_DIR}")
    
    def benchmark_integrity_latency(self):
        """Benchmark S2.1: Integrity Verification Latency."""
        print("\n[1/5] Benchmarking Integrity Verification Latency...")
        print("-" * 70)
        
        genome_sizes = {
            'Small (1KB)': self._create_genome_of_size(1_000),
            'Medium (10KB)': self._create_genome_of_size(10_000),
            'Large (100KB)': self._create_genome_of_size(100_000),
            'XLarge (1MB)': self._create_genome_of_size(1_000_000)
        }
        
        results = {}
        
        for label, genome in genome_sizes.items():
            print(f"  Testing {label}...", end=" ")
            
            # Warm-up
            for _ in range(100):
                genome.verify_integrity()
            
            # Actual benchmark
            times = timeit.repeat(
                lambda: genome.verify_integrity(),
                repeat=10000,
                number=1
            )
            
            times_ms = [t * 1000 for t in times]
            
            results[label] = {
                'mean_ms': mean(times_ms),
                'std_ms': stdev(times_ms),
                'min_ms': min(times_ms),
                'max_ms': max(times_ms)
            }
            
            print(f"✓ Mean: {results[label]['mean_ms']:.2f}ms")
        
        self.results['integrity_latency'] = results
        
        # Print table
        print("\nResults Table (Integrity Verification Latency):")
        print("-" * 70)
        print(f"{'Genome Size':<15} {'Mean (ms)':<12} {'Std (ms)':<12} {'Min (ms)':<12} {'Max (ms)':<12}")
        print("-" * 70)
        for label, data in results.items():
            print(f"{label:<15} {data['mean_ms']:<12.2f} {data['std_ms']:<12.2f} "
                  f"{data['min_ms']:<12.2f} {data['max_ms']:<12.2f}")
        print("-" * 70)
    
    def benchmark_hash_algorithms(self):
        """Benchmark S2.1.1: Hash Algorithm Comparison."""
        print("\n[2/5] Benchmarking Hash Algorithm Comparison...")
        print("-" * 70)
        
        # Create standard 10KB genome
        genome_data = self._create_genome_data(10_000)
        
        algorithms = {
            'SHA-256': self._benchmark_sha256,
            'SHA-1': self._benchmark_sha1,
        }
        
        # Add xxhash if available
        try:
            import xxhash
            algorithms['xxHash'] = self._benchmark_xxhash
        except ImportError:
            print("  Note: xxhash not available, skipping comparison")
        
        results = {}
        
        for name, hash_func in algorithms.items():
            print(f"  Testing {name}...", end=" ")
            
            times = timeit.repeat(
                lambda: hash_func(genome_data),
                repeat=10000,
                number=1
            )
            
            times_ms = [t * 1000 for t in times]
            results[name] = mean(times_ms)
            
            print(f"✓ {results[name]:.2f}ms")
        
        self.results['hash_algorithms'] = results
        
        print("\nResults Table (Hash Algorithm Comparison):")
        print("-" * 70)
        print(f"{'Algorithm':<15} {'Latency (ms)':<15}")
        print("-" * 70)
        for name, latency in results.items():
            print(f"{name:<15} {latency:<15.2f}")
        print("-" * 70)
    
    async def benchmark_collective_scaling(self):
        """Benchmark S2.2: Collective Resonance Scalability."""
        print("\n[3/5] Benchmarking Collective Resonance Scaling...")
        print("-" * 70)
        
        node_counts = [10, 100, 1000, 10000]
        results_sync = {}
        results_async = {}
        
        for n in node_counts:
            print(f"  Testing {n} nodes...")
            
            # Create collective
            collective = CollectiveIntelligence()
            for i in range(n):
                node = ResonanceNode(f'node_{i}', base_frequency=1.0 + i*0.1)
                collective.add_node(node)
            
            # Benchmark synchronous (simulated)
            print(f"    Synchronous...", end=" ")
            sync_times = []
            for _ in range(100):
                start = time.perf_counter()
                # Simulate synchronous processing
                responses = []
                for node in collective.nodes.values():
                    responses.append(node.resonate(7.5))
                _ = sum(responses) / len(responses)
                elapsed = time.perf_counter() - start
                sync_times.append(elapsed)
            
            results_sync[n] = mean(sync_times) * 1000  # ms
            print(f"✓ {results_sync[n]:.2f}ms")
            
            # Benchmark asynchronous
            print(f"    Asynchronous...", end=" ")
            async_times = []
            for _ in range(100):
                start = time.perf_counter()
                await collective.broadcast_wave(7.5)
                elapsed = time.perf_counter() - start
                async_times.append(elapsed)
            
            results_async[n] = mean(async_times) * 1000  # ms
            print(f"✓ {results_async[n]:.2f}ms")
        
        self.results['collective_scaling'] = {
            'synchronous': results_sync,
            'asynchronous': results_async
        }
        
        # Print table
        print("\nResults Table (Collective Resonance Scaling):")
        print("-" * 70)
        print(f"{'Nodes':<10} {'Sync (ms)':<15} {'Async (ms)':<15} {'Speedup':<10}")
        print("-" * 70)
        for n in node_counts:
            speedup = results_sync[n] / results_async[n]
            print(f"{n:<10} {results_sync[n]:<15.2f} {results_async[n]:<15.2f} {speedup:<10.1f}x")
        print("-" * 70)
    
    def benchmark_presence_memory(self):
        """Benchmark S2.3: Presence Layer Memory Usage."""
        print("\n[4/5] Benchmarking Presence Layer Memory...")
        print("-" * 70)
        
        decision_counts = [100, 1000, 10000, 100000, 1000000]
        
        # Test with naive list
        print("  Testing naive list implementation...")
        results_list = self._measure_presence_memory(decision_counts, use_deque=False)
        
        # Test with bounded deque
        print("  Testing bounded deque implementation...")
        results_deque = self._measure_presence_memory(decision_counts, use_deque=True)
        
        self.results['presence_memory'] = {
            'list': results_list,
            'deque': results_deque
        }
        
        # Print table
        print("\nResults Table (Presence Layer Memory Usage):")
        print("-" * 70)
        print(f"{'Decisions':<15} {'List (KB)':<15} {'Deque (KB)':<15}")
        print("-" * 70)
        for count in decision_counts:
            print(f"{count:<15,} {results_list[count]:<15.1f} {results_deque[count]:<15.1f}")
        print("-" * 70)
    
    async def benchmark_high_load(self):
        """Benchmark S3.3: High Load Stability."""
        print("\n[5/5] Benchmarking High Load Stability...")
        print("-" * 70)
        
        # Create runtime
        genome = GenomeBuilder.create_default()
        genome.seal()
        runtime = HopeGenomeRuntime(genome, enable_collective=False)
        
        # Generate 10,000 decision contexts
        print("  Generating 10,000 decision contexts...")
        contexts = [
            DecisionContext(
                action_type='read_file',
                target=f'/data/file_{i}.txt',
                intent='high load test',
                risk_level=RiskLevel.LOW,
                emotional_state=EmotionalState()
            )
            for i in range(10000)
        ]
        
        # Process concurrently
        print("  Processing decisions concurrently...")
        start = time.time()
        decisions = await asyncio.gather(*[
            runtime.decide(ctx) for ctx in contexts
        ])
        elapsed = time.time() - start
        
        # Verify all correct
        all_allow = all(d == EthicsDecision.ALLOW for d in decisions)
        
        throughput = 10000 / elapsed
        
        self.results['high_load'] = {
            'total_decisions': 10000,
            'elapsed_seconds': elapsed,
            'throughput_per_second': throughput,
            'all_correct': all_allow,
            'integrity_maintained': runtime.integrity_guard.verify_or_raise() is None
        }
        
        print(f"  ✓ Processed 10,000 decisions in {elapsed:.2f}s")
        print(f"  ✓ Throughput: {throughput:.0f} decisions/second")
        print(f"  ✓ All decisions correct: {all_allow}")
        print(f"  ✓ Integrity maintained: True")
    
    def save_results(self):
        """Save all results to JSON."""
        output_file = RESULTS_DIR / "benchmark_results.json"
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n✓ Results saved to: {output_file}")
    
    def generate_plots(self):
        """Generate all plots for supplementary material."""
        if not PLOTTING_AVAILABLE:
            print("Plotting libraries not available. Skipping plot generation.")
            return
        
        print("\nGenerating plots...")
        print("-" * 70)
        
        # Set style
        sns.set_style("whitegrid")
        
        # Plot 1: Integrity Latency
        self._plot_integrity_latency()
        
        # Plot 2: Collective Scaling
        self._plot_collective_scaling()
        
        # Plot 3: Memory Usage
        self._plot_memory_usage()
        
        print("✓ All plots generated in results/ directory")
    
    def _plot_integrity_latency(self):
        """Plot integrity verification latency."""
        if 'integrity_latency' not in self.results:
            return
        
        data = self.results['integrity_latency']
        labels = list(data.keys())
        means = [data[l]['mean_ms'] for l in labels]
        stds = [data[l]['std_ms'] for l in labels]
        
        plt.figure(figsize=(10, 6))
        plt.bar(labels, means, yerr=stds, capsize=5, alpha=0.7)
        plt.xlabel('Genome Size')
        plt.ylabel('Latency (ms)')
        plt.title('Integrity Verification Latency')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / 'integrity_latency.png', dpi=300)
        plt.close()
        
        print("  ✓ integrity_latency.png")
    
    def _plot_collective_scaling(self):
        """Plot collective scaling comparison."""
        if 'collective_scaling' not in self.results:
            return
        
        data = self.results['collective_scaling']
        nodes = sorted(data['synchronous'].keys())
        sync = [data['synchronous'][n] for n in nodes]
        async_vals = [data['asynchronous'][n] for n in nodes]
        
        plt.figure(figsize=(10, 6))
        plt.plot(nodes, sync, 'o-', label='Synchronous', linewidth=2)
        plt.plot(nodes, async_vals, 's-', label='Asynchronous', linewidth=2)
        plt.xlabel('Number of Nodes')
        plt.ylabel('Latency (ms)')
        plt.title('Collective Resonance Scaling: Sync vs. Async')
        plt.legend()
        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / 'collective_scaling.png', dpi=300)
        plt.close()
        
        print("  ✓ collective_scaling.png")
    
    def _plot_memory_usage(self):
        """Plot memory usage comparison."""
        if 'presence_memory' not in self.results:
            return
        
        data = self.results['presence_memory']
        decisions = sorted(data['list'].keys())
        list_mem = [data['list'][d] for d in decisions]
        deque_mem = [data['deque'][d] for d in decisions]
        
        plt.figure(figsize=(10, 6))
        plt.plot(decisions, list_mem, 'o-', label='Unbounded List', linewidth=2)
        plt.plot(decisions, deque_mem, 's-', label='Bounded Deque', linewidth=2)
        plt.xlabel('Number of Decisions')
        plt.ylabel('Memory Usage (KB)')
        plt.title('Presence Layer Memory: List vs. Deque')
        plt.legend()
        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / 'memory_usage.png', dpi=300)
        plt.close()
        
        print("  ✓ memory_usage.png")
    
    # Helper methods
    
    def _create_genome_of_size(self, target_bytes: int) -> HopeGenome:
        """Create a genome with approximately target_bytes size."""
        genome = GenomeBuilder.create_default()
        
        # Add padding to reach target size
        padding_size = max(0, target_bytes - len(json.dumps(genome.to_dict())))
        genome.metadata['padding'] = 'X' * padding_size
        
        genome.seal()
        return genome
    
    def _create_genome_data(self, target_bytes: int) -> bytes:
        """Create genome data for hashing benchmarks."""
        genome = self._create_genome_of_size(target_bytes)
        data = json.dumps(genome.to_dict(), sort_keys=True)
        return data.encode('utf-8')
    
    def _benchmark_sha256(self, data: bytes) -> str:
        """Compute SHA-256 hash."""
        import hashlib
        return hashlib.sha256(data).hexdigest()
    
    def _benchmark_sha1(self, data: bytes) -> str:
        """Compute SHA-1 hash."""
        import hashlib
        return hashlib.sha1(data).hexdigest()
    
    def _benchmark_xxhash(self, data: bytes) -> str:
        """Compute xxHash hash."""
        import xxhash
        return xxhash.xxh64(data).hexdigest()
    
    def _measure_presence_memory(
        self,
        decision_counts: List[int],
        use_deque: bool
    ) -> Dict[int, float]:
        """Measure memory usage for presence layer."""
        results = {}
        
        for count in decision_counts:
            # Create modified presence layer
            genome = GenomeBuilder.create_default()
            genome.seal()
            
            if use_deque:
                # Use bounded deque
                state = {
                    'emotional_trace': deque(maxlen=1000),
                    'decision_trace': deque(maxlen=1000),
                    'resonance_history': [],
                    'awakening_level': 0.0
                }
            else:
                # Use unbounded list
                state = {
                    'emotional_trace': [],
                    'decision_trace': [],
                    'resonance_history': [],
                    'awakening_level': 0.0
                }
            
            # Simulate decisions
            for i in range(count):
                entry = {
                    'timestamp': time.time(),
                    'emotional_state': {
                        'arousal': 0.5,
                        'valence': 0.5,
                        'dominance': 0.5
                    }
                }
                state['emotional_trace'].append(entry)
                state['decision_trace'].append({
                    'timestamp': time.time(),
                    'action_type': 'test',
                    'decision': 'ALLOW'
                })
            
            # Force garbage collection
            gc.collect()
            
            # Measure memory
            memory_bytes = sys.getsizeof(state['emotional_trace'])
            memory_bytes += sys.getsizeof(state['decision_trace'])
            
            results[count] = memory_bytes / 1024  # KB
        
        return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Hope Genome Benchmark Suite')
    parser.add_argument(
        '--test',
        choices=['all', 'integrity', 'collective', 'memory', 'load'],
        default='all',
        help='Which benchmark to run'
    )
    parser.add_argument(
        '--generate-plots',
        action='store_true',
        help='Generate plots after benchmarks'
    )
    
    args = parser.parse_args()
    
    suite = BenchmarkSuite()
    
    if args.test == 'all':
        suite.run_all()
    elif args.test == 'integrity':
        suite.benchmark_integrity_latency()
        suite.benchmark_hash_algorithms()
        suite.save_results()
    elif args.test == 'collective':
        asyncio.run(suite.benchmark_collective_scaling())
        suite.save_results()
    elif args.test == 'memory':
        suite.benchmark_presence_memory()
        suite.save_results()
    elif args.test == 'load':
        asyncio.run(suite.benchmark_high_load())
        suite.save_results()
    
    if args.generate_plots:
        suite.generate_plots()


if __name__ == '__main__':
    main()
