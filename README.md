# Regime-Stonks-RL

**Tear open market regimes and train RL agents to thrive in the chaos.**

A config-driven market simulation framework for testing trading agents across different market regimes using high-frequency (1-minute) and daily market data.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

---

## 🚀 Overview

Regime-Stonks-RL is a minimal yet powerful simulation engine designed for:
- **Multi-agent trading simulations** with configurable strategies (hedgers, CTAs, spec buyers, discretionary traders)
- **Regime-based backtesting** using user-defined or generated market regime labels
- **High-frequency data support** with 1-minute bars and daily aggregates
- **Flexible execution modeling** with configurable slippage and market impact
- **Reproducible experiments** with deterministic, seedable simulations

This framework enables researchers and traders to understand how different trading strategies perform under various market conditions without the complexity of a full order book simulation.

---

## ✨ Key Features

### 🎯 **Multi-Agent Framework**
- Run multiple trading agents simultaneously
- Each agent operates independently with its own state and strategy
- Support for various agent types: hedgers, trend followers, mean-reversion strategies, and more

### 📊 **Flexible Data Support**
- **1-minute bars**: High-frequency intraday data for precise execution timing
- **Daily bars**: Macro signals and longer-term trend indicators
- **News sentiment** (optional): Daily news text data aligned by date
- Multi-asset support: stocks, FX, crypto

### 🎮 **Config-Driven Design**
- All simulation parameters defined in YAML/JSON configuration files
- Easy to modify and version control your experiments
- No code changes needed to test different scenarios

### 🎭 **Market Regime Modeling**
- Define custom market regimes (trending, mean-reverting, volatile, calm, etc.)
- Test agent performance across different market conditions
- Understand which strategies work in which regimes

### 💹 **Realistic Execution Modeling**
- Configurable slippage per share
- Linear market impact based on order size
- Liquidity-aware execution without full order book complexity

### 🔬 **Comprehensive Metrics**
- Per-minute P&L tracking
- Agent inventory traces
- Price path visualization
- Customizable metric collection

---

## 📁 Repository Structure

```
Regime-Stonks-RL/
├── README.md                  # This file
├── LICENSE                    # Apache 2.0 License
├── base-agent.py             # Base agent interface definition
├── set-up-example.py         # Example simulation step logic
├── example_sim.yaml          # Example configuration file
└── observation.json          # Sample observation format
```

### Core Files

#### `base-agent.py`
Defines the agent interface that all trading agents must implement:
```python
class BaseAgent:
    def reset(self, initial_state) -> None: ...
    def observe(self, obs) -> None: ...
    def act(self) -> Action  # {'asset': 'SPY', 'type': 'target', 'target_shares': 100}
    def on_fill(self, fill_info) -> None: ...
```

#### `set-up-example.py`
Demonstrates the simulation step logic:
1. Build observations for each agent
2. Collect actions from all agents
3. Execute actions using the execution model
4. Update agent states with fill information
5. Record metrics for analysis

#### `example_sim.yaml`
Sample configuration file showing all available parameters

#### `observation.json`
Example observation structure passed to agents

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip or conda package manager

### Basic Setup

1. **Clone the repository:**
```bash
git clone https://github.com/avimiami/Regime-Stonks-RL.git
cd Regime-Stonks-RL
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

> **Note:** If `requirements.txt` doesn't exist yet, typical dependencies include:
> - `numpy`
> - `pandas`
> - `pyyaml`
> - `matplotlib` (for visualization)
> - `gymnasium` or `gym` (if using RL training)

3. **Prepare your data:**
   - Create `data/minute/` directory for 1-minute bar CSVs
   - Create `data/daily/` directory for daily bar CSVs
   - (Optional) Create `data/news/` for news sentiment data
   - (Optional) Create `data/regimes/` for regime label files

---

## 🎯 Quick Start

### 1. Configuration

Create or modify a simulation config file (YAML format):

```yaml
seed: 42

assets:
  - symbol: SPY
    minute_path: data/minute/SPY_1m.csv
    daily_path: data/daily/SPY_daily.csv

start:
  date: 2024-01-01
  initial_cash: 1000000
  initial_positions:
    SPY: 0

simulation:
  start_time: "09:30"
  end_time: "16:00"
  minute_bars_per_day: 390

execution_model:
  slippage_per_share: 0.0001      # Fraction of price
  impact_coefficient: 1e-6         # Linear impact per share
  liquidity_reference: 100000     # Reference liquidity in shares

regimes:
  regime_path: data/regimes/SPY_regimes.csv

agents:
  - name: hedger_1
    type: Hedger
    params:
      target_shares: 1000
      horizon_minutes: 240
      max_aggressiveness: 0.2
  
  - name: cta_1
    type: TrendCTA
    params:
      lookback: 60
      entry_threshold: 2.0
      exit_threshold: 1.0

metrics:
  save_path: runs/last_run/
  per_minute: true
```

### 2. Data Format

**Minute Bar CSV Format:**
```csv
datetime,open,high,low,close,volume
2024-01-02 09:30:00,430.12,430.50,429.80,430.00,12000
2024-01-02 09:31:00,430.00,430.25,429.95,430.15,8500
...
```

**Daily Bar CSV Format:**
```csv
date,open,high,low,close,volume
2024-01-02,430.00,435.50,429.00,434.20,85000000
...
```

**Regime Labels CSV Format:**
```csv
date,regime
2024-01-02,trend
2024-01-03,trend
2024-01-04,mean_revert
...
```

### 3. Implementing an Agent

Extend the `BaseAgent` class:

```python
class MyCustomAgent(BaseAgent):
    def __init__(self, name, params):
        self.name = name
        self.params = params
        self.position = 0
        self.cash = 0
    
    def reset(self, initial_state):
        """Initialize agent with starting conditions."""
        self.cash = initial_state['cash']
        self.position = initial_state.get('position', 0)
    
    def observe(self, obs):
        """Receive market observation."""
        self.last_obs = obs
        self.current_price = obs['bar']['close']
        self.features = obs['features']
        self.regime = obs['regime']
    
    def act(self):
        """Generate trading action."""
        # Your strategy logic here
        target_shares = self.compute_target_position()
        
        return {
            'asset': self.last_obs['asset'],
            'type': 'target',
            'target_shares': target_shares
        }
    
    def on_fill(self, fill_info):
        """Update state after order execution."""
        self.position += fill_info['shares_filled']
        self.cash -= fill_info['shares_filled'] * fill_info['fill_price']
```

### 4. Running a Simulation

```python
# Load configuration
with open('example_sim.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize environment and agents
env = MarketEnv(config)
agents = create_agents_from_config(config['agents'])

# Run simulation
for minute_bar in env.iter_bars():
    # Build observations
    for agent in agents:
        obs = build_obs(agent, minute_bar, features, regime)
        agent.observe(obs)
    
    # Collect actions
    actions = {agent.name: agent.act() for agent in agents}
    
    # Execute and update
    fills = execution_model.execute(actions, minute_bar, liquidity_params)
    for fill in fills:
        agent = agent_lookup[fill.agent]
        agent.on_fill(fill)
    
    # Record metrics
    save_minute_metrics(minute_bar.time, agents, metrics_store)
```

---

## 📊 Observation Format

Each agent receives observations in the following structure:

```json
{
  "datetime": "2024-01-02T10:15:00",
  "asset": "SPY",
  "bar": {
    "open": 430.12,
    "high": 430.5,
    "low": 429.8,
    "close": 430.0,
    "volume": 12000
  },
  "features": {
    "1m_return": 0.0003,
    "5m_momentum": 0.002,
    "60m_vol": 0.0015,
    "daily_return": -0.01,
    "news_sentiment": 0.2
  },
  "regime": "trend",
  "inventory": 200,
  "cash": 950000
}
```

**Fields:**
- `datetime`: Current timestamp
- `asset`: Asset symbol
- `bar`: OHLCV data for current minute
- `features`: Computed technical indicators and signals
- `regime`: Current market regime label
- `inventory`: Agent's current position in shares
- `cash`: Agent's current cash balance

---

## 🎭 Market Regimes

Regimes help categorize market behavior and test strategy robustness:

### Common Regime Types
- **trend**: Persistent directional movement
- **mean_revert**: Range-bound, oscillating behavior
- **volatile**: High volatility, choppy movements
- **calm**: Low volatility, stable prices
- **breakout**: Transition from calm to trending
- **crisis**: Extreme volatility, correlation breakdown

### Defining Regimes

**Option 1: Manual CSV**
```csv
date,regime
2024-01-02,trend
2024-01-03,trend
2024-01-04,volatile
```

**Option 2: Algorithmic Generation**
Use volatility, returns, or other metrics to automatically label regimes:
```python
def classify_regime(df):
    vol = df['returns'].rolling(20).std()
    if vol > threshold_high:
        return 'volatile'
    elif abs(df['returns'].mean()) > trend_threshold:
        return 'trend'
    else:
        return 'mean_revert'
```

---

## 🔧 Execution Model

The framework uses a simplified execution model suitable for research:

### Slippage Model
```python
fill_price = bar_price * (1 + slippage_per_share * sign(order))
```

### Market Impact Model
```python
impact = (order_size / liquidity_reference) * impact_coefficient * price
fill_price = bar_price + impact
```

### Configuration Parameters

- `slippage_per_share`: Base slippage as fraction of price (e.g., 0.0001 = 1 bp)
- `impact_coefficient`: Scales market impact by order size
- `liquidity_reference`: Normalizes impact calculation (e.g., 100,000 shares)

---

## 📈 Metrics and Analysis

### Agent-Level Metrics
- **Cumulative P&L**: Total profit/loss over time
- **Sharpe Ratio**: Risk-adjusted returns
- **Max Drawdown**: Largest peak-to-trough decline
- **Inventory Trace**: Position size over time
- **Trade Count**: Number of trades executed
- **Fill Rate**: Percentage of desired orders filled

### Regime-Specific Analysis
- P&L by regime type
- Win rate by regime
- Average position size by regime
- Regime transition behavior

### System-Level Metrics
- Total market volume
- Price impact statistics
- Cross-agent correlation

---

## 🎨 Example Agent Types

### 1. **Hedger**
Executes a target position over a specified horizon
- Parameters: `target_shares`, `horizon_minutes`, `max_aggressiveness`
- Use case: Minimizing market impact of large orders

### 2. **Trend CTA**
Follows momentum signals with threshold-based entries/exits
- Parameters: `lookback`, `entry_threshold`, `exit_threshold`
- Use case: Capturing persistent trends

### 3. **Spec Buyer**
Opportunistic buying on dips with mean-reversion logic
- Parameters: `buy_threshold`, `sell_threshold`, `max_position`
- Use case: Value investing, contrarian strategies

### 4. **Old Hands** (Discretionary)
Rule-based or ML-driven decision making with regime awareness
- Parameters: Custom per strategy
- Use case: Complex multi-factor strategies

---

## 🧪 Testing and Validation

### Deterministic Execution
Set a seed for reproducibility:
```yaml
seed: 42
```

All random operations (data sampling, agent initialization) will be deterministic.

### Backtesting Workflow
1. Split data into train/test periods
2. Define regimes for historical data
3. Configure agents with different strategies
4. Run simulation on test period
5. Compare metrics across agents and regimes

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Areas for Contribution
- New agent implementations
- Additional execution models (e.g., VWAP, TWAP)
- Enhanced regime detection algorithms
- Visualization tools
- Documentation improvements
- Bug fixes

### Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with clear commit messages
4. Add tests if applicable
5. Submit a pull request

---

## 📋 Design Decisions & Assumptions

### Core Principles

1. **No Order Book**: Simplified execution model at bar-level with slippage/impact functions instead of full LOB matching
2. **Config-Driven**: All parameters (agents, assets, initial conditions) defined in configuration files
3. **Agent Abstraction**: Clean API (observe → act → on_fill) allows easy agent development
4. **Deterministic**: Seedable randomness for reproducible research
5. **Multi-Asset**: Support for stocks, FX, crypto with unified data format
6. **Regime-Aware**: First-class support for regime labels and regime-specific analysis

### Data Assumptions

- **Minute bars** are the primary timestep (though other frequencies are possible)
- **Daily bars** provide macro context and signals
- **News text** (optional) is aligned by date
- Data is pre-processed and cleaned (no real-time data handling)

### Execution Assumptions

- Orders execute at the close of the current bar (no intra-bar fills)
- No partial fills (though this can be extended)
- Linear market impact model
- No transaction costs beyond slippage/impact (can be added)

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by research in regime-based trading and multi-agent market simulation
- Built for the quantitative trading and reinforcement learning communities
- Designed to bridge the gap between simplistic backtesting and complex market simulators

---

## 📞 Support and Contact

- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/avimiami/Regime-Stonks-RL/issues)
- **Discussions**: Join community discussions in the repository

---

## 🗺️ Roadmap

### Future Enhancements
- [ ] Add full implementation of agent types (hedger, CTA, etc.)
- [ ] Implement visualization dashboard for metrics
- [ ] Add RL training integration (PPO, SAC, etc.)
- [ ] Support for options and derivatives
- [ ] Multi-asset portfolio optimization
- [ ] Real-time data streaming support
- [ ] Web UI for configuration and monitoring
- [ ] Distributed simulation for large-scale experiments

---

**Happy Trading! May your agents learn to thrive in any regime. 📈🤖**
