# RL Glossary — Open Duck Mini Context

Terms defined for biped locomotion RL. Each definition is brief, technical, and tied to this project where applicable.

---

**Policy** — The neural network that maps observations to actions. In this project: takes ~60-dim observation vector → outputs 14 joint angle targets. Parameterized by weights θ, updated by PPO.

**Rollout** — A batch of experience collected by running the current policy in the environment for T steps across K parallel envs. The raw data PPO trains on. Not stored long-term — used once per update then discarded.

**Episode** — One continuous run from env.reset() to termination (fall, timeout). In this project: healthy episodes should last 300-450 steps. Current broken training produces ~47-step episodes (robot falls immediately).

**Observation (obs)** — The state information the policy receives each timestep. Typically: joint angles, joint velocities, base orientation, base velocity, commanded velocity, previous actions, gravity vector. A flat float vector.

**Action** — The policy's output each timestep. Here: 14 continuous values representing desired joint positions. Scaled from network output range ([-1,1]) to actual joint angle ranges. Applied as PD control targets in MuJoCo.

**Reward** — Scalar feedback signal per timestep. Sum of weighted components (tracking, alive, imitation, penalties). The ONLY learning signal — if the reward is wrong, the policy learns wrong behavior. Period.

**Reward Shaping** — Designing reward components and their weights to guide learning toward desired behavior. The most fragile part of the pipeline. In this project: the reward was catastrophically mis-shaped (alive=7407%, imitation=1.2%), causing the freeze-and-fall failure.

**Termination** — Condition that ends an episode. Typically: torso height below threshold, torso angle too far from vertical, or max steps reached. Early termination signals "this behavior is fatally bad."

**Checkpoint** — Saved snapshot of policy weights + optimizer state at a given training step. Allows resuming training or deploying a specific version. Should be saved periodically (e.g., every 1M steps).

**Domain Randomization** — Varying simulation parameters (mass, friction, motor strength, noise) during training so the policy generalizes to real hardware. Without it, sim-to-real transfer typically fails. Status in this project: UNKNOWN (not verified in code).

**Sim-to-Real** — Deploying a policy trained in simulation onto physical hardware. The fundamental challenge: simulation is always an approximation. Gaps include actuator dynamics, contact physics, sensor noise, and latency.

**PPO (Proximal Policy Optimization)** — The optimization algorithm. Collects rollout data, computes advantages, updates policy with clipped objective to prevent destructively large updates. Standard for locomotion RL. Uses: policy loss (clipped surrogate), value loss, entropy bonus.

**Entropy** — Measure of policy randomness. High entropy = exploring many actions. Low entropy = deterministic (committed to one strategy). In this project: entropy collapsed to -0.043 (effectively zero exploration). Healthy range: 0.5-2.0.

**Clipping (PPO)** — The core PPO mechanism. The ratio π_new/π_old is clipped to [1-ε, 1+ε]. Prevents the policy from changing too much in one update. In this project: ε=0.15 (fixed value).

**Gradient Norm** — Magnitude of the gradient vector. Clipped to prevent explosion (unstable, divergent updates). In this project: clipped to 0.5 (fixed value). If gradients consistently hit the clip ceiling, learning rate may be too high.

**Value Function (Critic)** — A second neural network that estimates "how good is this state?" Used to compute advantages (how much better was this action than expected). Trained alongside the policy. If the value function is inaccurate, advantage estimates are noisy → unstable learning.

**Exploration** — Trying new, potentially suboptimal actions to discover better strategies. Maintained by entropy bonus in PPO. Without sufficient exploration, the policy gets stuck in local optima (like "freeze and fall").

**Exploitation** — Using the current best strategy to maximize reward. The tension between exploration and exploitation is fundamental. Too much exploitation too early = premature convergence. Too much exploration = slow learning.

**GAE (Generalized Advantage Estimation)** — Method to compute advantages from rollout data. Balances bias and variance using parameters γ (discount) and λ. In this project: γ=0.99 gives ~100-step effective horizon.

**Reference Motion** — Pre-recorded joint trajectories of desired walking behavior. Used by the imitation reward component. The policy gets reward for matching these trajectories. 243 reference trajectories documented in fix doc.

**Reward Hacking** — When the policy finds an unintended way to maximize reward that doesn't match the designer's intent. Example: collecting alive bonus by standing still instead of walking. The freeze-and-fall behavior IS reward hacking.
