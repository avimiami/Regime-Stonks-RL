def step(minute_bar):
    # 1) Build obs for each agent
    for agent in agents:
        obs = build_obs(agent, minute_bar, features, regime)
        agent.observe(obs)

    # 2) Collect actions
    actions = {agent.name: agent.act() for agent in agents}

    # 3) Execute actions using execution_model -> fills
    fills = execution_model.execute(actions, minute_bar, liquidity_params)

    # 4) Update agent state & compute realized pnl
    for fill in fills:
        agent = agent_lookup[fill.agent]
        agent.on_fill(fill)
        record_trade(fill)

    # 5) Save metrics (P&L, inventory) for this minute
    save_minute_metrics(minute_bar.time, agents, minute_metrics_store)

    # 6) Advance time / return observations for next step
