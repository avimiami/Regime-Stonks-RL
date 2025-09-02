# Regime-Stonks-RL
Tear open market regimes and train RL agents to thrive in the chaos.   > Config-driven simulation for 1-minute + daily data and daily news — run populations of hedgers, CTAs, spec buyers, and discretionary agents under user-defined regimes. 

all data is 1-minute and daily for stocks/FX/crypto, plus daily news text, no order book, and full control over regimes & signals. The repo lets you configure which agents to run, their starting conditions, and the environment parameters from YAML/JSON configs. It will produce the metrics/plots you requested (cumulative P&L per agent, inventory traces, price path, plus other useful agent-level metrics).

What this repo does (short)

A minimal simulation engine that replays 1-minute/daily market data + daily news, runs multiple configurable agents (hedger, trend CTA, spec buyer, old hands, etc.), uses a simple execution/slippage model (no order book), and outputs metrics and visualizations to compare agent outcomes across regimes and configurations.

Key design decisions / assumptions

Data frequency: 1-minute bars (primary) and daily bars (for macro signals), plus daily news text.

No LOB: there is no orderbook matching engine. Execution is modeled at bar-level with configurable slippage / impact functions.

User-provided regimes & signals: you provide regime labels & signal functions (or use the built-in simple regime generator).

Config-driven: all starting values (initial cash, positions, assets, agent list, environment) live in a config file.

Agent abstraction: each agent implements a small API (obs → action). Many agents can run simultaneously.

Deterministic / seedable: runs are reproducible when seeded.
