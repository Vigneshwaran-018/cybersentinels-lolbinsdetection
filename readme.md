# Cyber Sentinels LoLBINS: Advanced Endpoint Defense System

**Cyber Sentinels Detection System** - Advanced Endpoint Defense & Living-Off-The-Land (LOLBins) Detection

A comprehensive security solution designed to detect and prevent abuse of legitimate Windows binaries (Living-Off-The-Land binaries) used in modern cyber attacks. This system monitors process execution in real-time and identifies suspicious activities through pattern detection and risk scoring.

---

## 🎯 Overview

LOLBINS-X is an endpoint defense system built for the KTR Hackathon that focuses on detecting misuse of legitimate Windows binaries (LOLBins) that attackers commonly exploit. The system features:

- **Real-time Process Monitoring**: Continuously watches process execution and parent-child relationships
- **LOLBins Detection**: Identifies suspicious usage patterns of legitimate Windows tools
- **Risk Scoring Engine**: Calculates threat levels based on process behavior and context
- **Interactive Dashboard**: Provides visual monitoring and real-time threat alerts
- **Simulation Mode**: Test the system with synthetic attack scenarios
- **Forensic Timeline**: Generates forensic records for incident investigation

---

## 📁 Project Structure

```
lolbins/
├── main.py                      # Entry point - starts the engine
├── requirements.txt             # Python dependencies
├── forensics_timeline.json      # Forensic event log
├── config/                      # Configuration files
│   ├── settings.json           # Main settings & LOLBins list
│   ├── trusted_parents.json    # Trusted parent processes
│   └── loader.py               # Configuration loader
├── core/                        # Core engine modules
│   ├── engine.py               # Orchestrator - coordinates all components
│   ├── defense/                # Defense mechanisms
│   │   └── defender.py         # Blocking & response actions
│   ├── detection/              # Detection rules
│   │   └── lolbins_rules.py   # LOLBins detection patterns
│   ├── monitor/                # Process monitoring
│   │   ├── process_watcher.py # Main process monitoring loop
│   │   ├── command_parser.py  # Command-line parsing
│   │   ├── parent_tracker.py  # Process hierarchy tracking
│   │   ├── dedup.py            # Event deduplication
│   │   └── __init__.py
│   └── scoring/                # Risk scoring engine
│       ├── risk_engine.py      # Risk calculation & scoring
│       └── __init__.py
├── gui/                         # User interface
│   └── dashboard.py            # Tkinter dashboard
├── forensics/                   # Forensic analysis
│   └── timeline.py             # Forensic timeline generation
├── knowledge/                   # Knowledge base
│   └── lolbins_db.json        # LOLBins database
├── simulation/                  # Testing & simulation
│   ├── simulator.py            # Attack simulation engine
│   ├── datasets.json           # Simulation datasets
│   ├── benign/                 # Benign process samples
│   └── lolbin_attacks/         # Attack scenario samples
└── tests/                       # Test suite
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+**
- **Windows OS** (for process monitoring)
- **psutil** library

### Installation

1. **Clone/Navigate to the project directory:**
   ```bash
   cd "c:\Users\Vignesh\Desktop\ktr hackathon\lolbins"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings (optional):**
   Edit `config/settings.json` to customize monitored LOLBins and thresholds.

### Running the System

```bash
python main.py
```

This will:
1. Start the process monitoring engine
2. Load attack simulation scenarios
3. Launch the interactive dashboard GUI
4. Begin real-time threat detection and logging

---

## ⚙️ Configuration

### Main Settings (`config/settings.json`)

```json
{
  "defense_mode": "block",
  "risk_block_threshold": 60,
  "lolbins": [
    "powershell.exe",
    "cmd.exe",
    "certutil.exe",
    "rundll32.exe",
    "wmic.exe"
  ]
}
```

- **defense_mode**: `block` (active defense) or `monitor` (detection only)
- **risk_block_threshold**: Minimum risk score to trigger blocking (0-100)
- **lolbins**: List of monitored legitimate binaries

### Trusted Parents (`config/trusted_parents.json`)

Define parent processes that should not trigger alerts even when spawning LOLBins.

---

## 🔍 Core Components

### 1. **Process Watcher** (`core/monitor/process_watcher.py`)
- Continuously monitors Windows processes
- Captures command-line arguments and environment
- Tracks parent-child process relationships
- Deduplicates events to reduce noise

### 2. **LOLBins Detection** (`core/detection/lolbins_rules.py`)
Detection patterns include:
- PowerShell with encoded commands (`-enc`, `-encodedcommand`)
- CMD command execution (`/c`)
- Certutil abuse
- And more...

### 3. **Risk Scoring Engine** (`core/scoring/risk_engine.py`)
Calculates threat scores based on:
- Process characteristics
- Command-line indicators
- Parent process context
- Known attack patterns

### 4. **Defense Module** (`core/defense/defender.py`)
- Blocks high-risk processes
- Logs security events
- Generates alerts

### 5. **Dashboard GUI** (`gui/dashboard.py`)
- Real-time event monitoring
- Process tree visualization
- Risk score display
- System status and statistics

### 6. **Forensics** (`forensics/timeline.py`)
- Creates `forensics_timeline.json` for incident investigation
- Records all detected events with timestamps and context

---

## 📊 Risk Scoring

The risk engine assigns scores (0-100) based on:

| Factor | Score Impact |
|--------|--------------|
| Known LOLBins executable | +20-40 |
| Suspicious command arguments | +15-30 |
| Suspicious parent process | +10-25 |
| Encoded/obfuscated commands | +25-40 |
| Network communication attempts | +10-20 |

**Block Threshold**: Processes exceeding 60 points are blocked (configurable).

---

## 🎮 Simulation Mode

Test the system with synthetic attack scenarios:

```bash
# Run from Python
from simulation.simulator import run_simulation
run_simulation()
```

Simulation includes:
- Benign process samples
- LOLBins attack scenarios
- Pattern validation

---

## 📈 Forensic Analysis

All detected events are logged to `forensics_timeline.json` for later analysis:

```json
{
  "timestamp": "2026-01-30T10:30:45Z",
  "process": "powershell.exe",
  "pid": 1234,
  "command": "powershell.exe -enc <encoded_command>",
  "risk_score": 85,
  "threat_type": "Encoded Powershell",
  "action": "BLOCKED"
}
```

---

## 🛠️ Development

### Adding New Detection Rules

Edit `core/detection/lolbins_rules.py`:

```python
def detect_lolbins(event):
    suspicious = []
    
    name = event["name"].lower()
    cmd = " ".join(event["cmd"]).lower()
    
    # Add your custom detection logic
    if name == "your_lolbin.exe" and "suspicious_flag" in cmd:
        suspicious.append("Your custom threat description")
    
    return suspicious
```

### Adjusting Thresholds

Modify scoring weights in `core/scoring/risk_engine.py` to fine-tune detection sensitivity.

---

## 📝 Dependencies

- **psutil**: Cross-platform process monitoring library

See `requirements.txt` for full list.

---

## 🔐 Security Notes

- This system is designed for **Windows endpoints**
- Requires **administrator/elevated privileges** for full functionality
- Operating in `block` mode will actively prevent process execution
- Always test in a controlled environment first

---

## 📄 License & Attribution

This project was developed for the KTR Hackathon focusing on advanced endpoint defense techniques and LOLBins detection.

---

## 🤝 Support & Contribution

For issues, questions, or improvements:
1. Check existing documentation in code comments
2. Review the project structure for relevant modules
3. Test changes in simulation mode first

---

## 🎯 Key Features Summary

✅ Real-time process monitoring  
✅ Living-Off-The-Land binary detection  
✅ Risk-based threat scoring  
✅ Active defense & blocking  
✅ Interactive dashboard UI  
✅ Attack simulation & testing  
✅ Forensic timeline generation  
✅ Highly configurable  

---

**Last Updated**: January 30, 2026  
**System**: Cyber Sentinels Detection System v1.0
