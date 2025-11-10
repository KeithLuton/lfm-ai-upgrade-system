#!/usr/bin/env python3
"""
LFM AI UPGRADE SYSTEM - MONITORING DASHBOARD
============================================
Real-time monitoring and visualization of system performance

Copyright (C) 2025 Dr. Keith Luton. All rights reserved.
"""

import time
import json
import threading
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from typing import Dict, List, Optional

class LFMMonitoringDashboard:
    """Real-time monitoring dashboard for LFM AI Upgrade System"""
    
    def __init__(self, system=None, update_interval=1.0):
        self.system = system
        self.update_interval = update_interval
        self.running = False
        self.monitor_thread = None
        
        # Metrics storage
        self.metrics_history = {
            'operations_rate': deque(maxlen=100),
            'cache_hit_rate': deque(maxlen=100),
            'confidence_scores': deque(maxlen=100),
            'axiom_usage': deque(maxlen=100),
            'memory_usage': deque(maxlen=100),
            'timestamps': deque(maxlen=100)
        }
        
        # Performance thresholds
        self.thresholds = {
            'operations_rate': {'warning': 10000, 'critical': 1000},
            'cache_hit_rate': {'warning': 0.7, 'critical': 0.5},
            'confidence_scores': {'warning': 0.6, 'critical': 0.4}
        }
        
        # Alert system
        self.alerts = deque(maxlen=50)
        self.alert_counts = {'info': 0, 'warning': 0, 'critical': 0}
    
    def start_monitoring(self):
        """Start the monitoring thread"""
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            print("📊 Monitoring Dashboard Started")
    
    def stop_monitoring(self):
        """Stop the monitoring thread"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("📊 Monitoring Dashboard Stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                # Collect metrics
                metrics = self._collect_metrics()
                
                # Store metrics
                self._store_metrics(metrics)
                
                # Check thresholds
                self._check_thresholds(metrics)
                
                # Sleep
                time.sleep(self.update_interval)
                
            except Exception as e:
                self._add_alert('critical', f"Monitoring error: {e}")
    
    def _collect_metrics(self) -> Dict:
        """Collect current system metrics"""
        if self.system:
            diagnostics = self.system.system_diagnostics()
            
            metrics = {
                'timestamp': datetime.now(),
                'operations_rate': diagnostics['performance']['current_rate'],
                'cache_hit_rate': diagnostics['neural_tier1']['hit_rate'],
                'total_operations': diagnostics['system']['total_operations'],
                'physics_axioms': sum(diagnostics['physics_axioms'].values()),
                'ai_axioms': sum(diagnostics['ai_axioms'].values()),
                'reasoning_count': diagnostics['executive_tier2']['reasoning_count'],
                'uncertainty_acks': diagnostics['humility']['uncertainty_acknowledgments']
            }
        else:
            # Demo metrics if no system attached
            metrics = {
                'timestamp': datetime.now(),
                'operations_rate': np.random.uniform(50000, 150000),
                'cache_hit_rate': np.random.uniform(0.75, 0.95),
                'total_operations': int(time.time() * 1000) % 1000000,
                'physics_axioms': np.random.randint(100, 1000),
                'ai_axioms': np.random.randint(200, 2000),
                'reasoning_count': np.random.randint(10, 100),
                'uncertainty_acks': np.random.randint(0, 20)
            }
        
        return metrics
    
    def _store_metrics(self, metrics: Dict):
        """Store metrics in history"""
        self.metrics_history['timestamps'].append(metrics['timestamp'])
        self.metrics_history['operations_rate'].append(metrics['operations_rate'])
        self.metrics_history['cache_hit_rate'].append(metrics['cache_hit_rate'])
        
        # Calculate confidence (simplified)
        confidence = min(1.0, metrics['cache_hit_rate'] * 1.2)
        self.metrics_history['confidence_scores'].append(confidence)
        
        # Store axiom usage
        total_axioms = metrics['physics_axioms'] + metrics['ai_axioms']
        self.metrics_history['axiom_usage'].append(total_axioms)
    
    def _check_thresholds(self, metrics: Dict):
        """Check metrics against thresholds and generate alerts"""
        # Check operations rate
        if metrics['operations_rate'] < self.thresholds['operations_rate']['critical']:
            self._add_alert('critical', f"Operations rate critically low: {metrics['operations_rate']:.0f}/sec")
        elif metrics['operations_rate'] < self.thresholds['operations_rate']['warning']:
            self._add_alert('warning', f"Operations rate low: {metrics['operations_rate']:.0f}/sec")
        
        # Check cache hit rate
        if metrics['cache_hit_rate'] < self.thresholds['cache_hit_rate']['critical']:
            self._add_alert('critical', f"Cache hit rate critical: {metrics['cache_hit_rate']:.1%}")
        elif metrics['cache_hit_rate'] < self.thresholds['cache_hit_rate']['warning']:
            self._add_alert('warning', f"Cache hit rate low: {metrics['cache_hit_rate']:.1%}")
    
    def _add_alert(self, level: str, message: str):
        """Add an alert to the system"""
        alert = {
            'timestamp': datetime.now(),
            'level': level,
            'message': message
        }
        self.alerts.append(alert)
        self.alert_counts[level] += 1
    
    def get_dashboard_data(self) -> Dict:
        """Get current dashboard data for display"""
        if not self.metrics_history['timestamps']:
            return {'status': 'No data available'}
        
        current_time = self.metrics_history['timestamps'][-1]
        
        # Calculate statistics
        ops_rates = list(self.metrics_history['operations_rate'])
        cache_rates = list(self.metrics_history['cache_hit_rate'])
        confidence = list(self.metrics_history['confidence_scores'])
        
        dashboard = {
            'timestamp': current_time.isoformat(),
            'current': {
                'operations_rate': ops_rates[-1] if ops_rates else 0,
                'cache_hit_rate': cache_rates[-1] if cache_rates else 0,
                'confidence': confidence[-1] if confidence else 0,
                'axiom_usage': self.metrics_history['axiom_usage'][-1] if self.metrics_history['axiom_usage'] else 0
            },
            'statistics': {
                'avg_operations_rate': np.mean(ops_rates) if ops_rates else 0,
                'max_operations_rate': max(ops_rates) if ops_rates else 0,
                'min_operations_rate': min(ops_rates) if ops_rates else 0,
                'avg_cache_hit_rate': np.mean(cache_rates) if cache_rates else 0,
                'avg_confidence': np.mean(confidence) if confidence else 0
            },
            'trends': {
                'operations_trend': self._calculate_trend(ops_rates),
                'cache_trend': self._calculate_trend(cache_rates),
                'confidence_trend': self._calculate_trend(confidence)
            },
            'alerts': {
                'recent': list(self.alerts)[-5:],
                'counts': dict(self.alert_counts)
            }
        }
        
        return dashboard
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction"""
        if len(values) < 2:
            return 'stable'
        
        recent = values[-10:]
        if len(recent) < 2:
            return 'stable'
        
        # Simple linear regression
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]
        
        if slope > 0.01:
            return 'improving'
        elif slope < -0.01:
            return 'declining'
        else:
            return 'stable'
    
    def print_dashboard(self):
        """Print formatted dashboard to console"""
        dashboard = self.get_dashboard_data()
        
        if 'status' in dashboard:
            print(dashboard['status'])
            return
        
        # Clear screen (works on Unix/Linux/Mac)
        print('\033[2J\033[H', end='')
        
        print("="*80)
        print("LFM AI UPGRADE SYSTEM - MONITORING DASHBOARD".center(80))
        print(f"Time: {dashboard['timestamp']}".center(80))
        print("="*80)
        print()
        
        # Current metrics
        print("📊 CURRENT METRICS")
        print("-"*40)
        print(f"Operations Rate:  {dashboard['current']['operations_rate']:>12,.0f} ops/sec")
        print(f"Cache Hit Rate:   {dashboard['current']['cache_hit_rate']:>12.1%}")
        print(f"Confidence Score: {dashboard['current']['confidence']:>12.1%}")
        print(f"Axiom Usage:      {dashboard['current']['axiom_usage']:>12,}")
        print()
        
        # Statistics
        print("📈 STATISTICS")
        print("-"*40)
        print(f"Avg Operations:   {dashboard['statistics']['avg_operations_rate']:>12,.0f} ops/sec")
        print(f"Max Operations:   {dashboard['statistics']['max_operations_rate']:>12,.0f} ops/sec")
        print(f"Min Operations:   {dashboard['statistics']['min_operations_rate']:>12,.0f} ops/sec")
        print(f"Avg Cache Hit:    {dashboard['statistics']['avg_cache_hit_rate']:>12.1%}")
        print(f"Avg Confidence:   {dashboard['statistics']['avg_confidence']:>12.1%}")
        print()
        
        # Trends
        print("📉 TRENDS")
        print("-"*40)
        trends = dashboard['trends']
        symbols = {'improving': '↑', 'declining': '↓', 'stable': '→'}
        colors = {'improving': '\033[92m', 'declining': '\033[91m', 'stable': '\033[94m'}
        reset = '\033[0m'
        
        for metric, trend in trends.items():
            symbol = symbols.get(trend, '?')
            color = colors.get(trend, '')
            metric_name = metric.replace('_', ' ').title()
            print(f"{metric_name:20} {color}{symbol} {trend}{reset}")
        print()
        
        # Alerts
        if dashboard['alerts']['recent']:
            print("⚠️  RECENT ALERTS")
            print("-"*40)
            for alert in dashboard['alerts']['recent']:
                level_symbols = {'info': 'ℹ', 'warning': '⚠', 'critical': '🔴'}
                symbol = level_symbols.get(alert['level'], '?')
                print(f"{symbol} [{alert['timestamp'].strftime('%H:%M:%S')}] {alert['message']}")
            print()
        
        # Alert summary
        counts = dashboard['alerts']['counts']
        print("📋 ALERT SUMMARY")
        print("-"*40)
        print(f"Info:     {counts['info']:>6}")
        print(f"Warning:  {counts['warning']:>6}")
        print(f"Critical: {counts['critical']:>6}")
        print()
        
        # Humility reminder
        print("💭 EPISTEMIC HUMILITY")
        print("-"*40)
        reminders = [
            "Every problem is a learning opportunity",
            "Question assumptions continuously",
            "Seek external validation",
            "Maintain infinite curiosity",
            "Never stop improving"
        ]
        print(f"  \"{np.random.choice(reminders)}\"")
        print()
        print("="*80)
    
    def save_metrics(self, filepath: str):
        """Save metrics history to file"""
        metrics_data = {
            'timestamp': datetime.now().isoformat(),
            'metrics_history': {
                'operations_rate': list(self.metrics_history['operations_rate']),
                'cache_hit_rate': list(self.metrics_history['cache_hit_rate']),
                'confidence_scores': list(self.metrics_history['confidence_scores']),
                'axiom_usage': list(self.metrics_history['axiom_usage']),
                'timestamps': [t.isoformat() for t in self.metrics_history['timestamps']]
            },
            'alerts': [
                {
                    'timestamp': a['timestamp'].isoformat(),
                    'level': a['level'],
                    'message': a['message']
                } for a in self.alerts
            ],
            'alert_counts': dict(self.alert_counts)
        }
        
        with open(filepath, 'w') as f:
            json.dump(metrics_data, f, indent=2)
        
        print(f"📊 Metrics saved to {filepath}")

def run_dashboard_demo():
    """Run a demonstration of the monitoring dashboard"""
    print("Starting LFM Monitoring Dashboard Demo...")
    print("This will show simulated metrics for 30 seconds")
    print()
    
    # Create dashboard
    dashboard = LFMMonitoringDashboard()
    
    # Start monitoring
    dashboard.start_monitoring()
    
    # Run for 30 seconds, updating display every 2 seconds
    start_time = time.time()
    while time.time() - start_time < 30:
        time.sleep(2)
        dashboard.print_dashboard()
    
    # Stop monitoring
    dashboard.stop_monitoring()
    
    # Save metrics
    dashboard.save_metrics("dashboard_metrics.json")
    
    print("\nDashboard demo complete!")

if __name__ == "__main__":
    run_dashboard_demo()
