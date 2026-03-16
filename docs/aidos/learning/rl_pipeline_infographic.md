# RL Pipeline Infographic — Open Duck Mini

```
┌─────────────────────────────────────────────────────────────┐
│                    TRAINING PIPELINE OVERVIEW                │
└─────────────────────────────────────────────────────────────┘

 ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
 │  MuJoCo  │────▶│  Rollout  │────▶│   PPO    │────▶│ Updated  │
 │   Env    │     │  Buffer   │     │  Update  │     │  Policy  │
 └──────────┘     └──────────┘     └──────────┘     └──────────┘
      │                                                    │
      └────────────────────────────────────────────────────┘
                         repeat for N million steps


 ┌─────────────────────────────────────────────────────────────┐
 │                    SINGLE ROLLOUT STEP                       │
 └─────────────────────────────────────────────────────────────┘

  Env State ──▶ Observation (obs) ──▶ Policy Network ──▶ Action
       │                                                    │
       │           ┌──────────────────────────────┐         │
       └───────────│  MuJoCo Physics Step (dt)     │◀───────┘
                   │  • apply joint torques         │
                   │  • simulate contacts           │
                   │  • advance time                │
                   └──────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Compute Reward   │
                    │   Check Done       │
                    └───────────────────┘


 ┌─────────────────────────────────────────────────────────────┐
 │                    REWARD COMPUTATION                        │
 └─────────────────────────────────────────────────────────────┘

  reward = clip( sum_of_components * dt, lower_bound, upper_bound )

  Components:
  ┌─────────────────┬────────┬──────────────────────────────┐
  │ tracking_lin_vel │  +2.5  │ match commanded velocity     │
  │ tracking_ang_vel │  +6.0  │ match commanded turn rate    │
  │ imitation        │  +5.0* │ match reference motion       │
  │ alive            │  +2.0* │ bonus for not falling        │
  │ torques          │ -0.001 │ penalize high torque         │
  │ action_rate      │  -0.1* │ penalize jerky actions       │
  │ stand_still      │  -2.0* │ penalize not moving          │
  └─────────────────┴────────┴──────────────────────────────┘
  * = values after Fix #2 (pre-fix values are catastrophically wrong)

  CRITICAL BUG (Fix #1):
  ┌───────────────────────────────────────────────────────┐
  │ BROKEN: clip(reward, 0.0, 10000)  ← mistakes are FREE│
  │ FIXED:  clip(reward, -10000, 10000) ← mistakes HURT  │
  └───────────────────────────────────────────────────────┘


 ┌─────────────────────────────────────────────────────────────┐
 │                    PPO UPDATE CYCLE                          │
 └─────────────────────────────────────────────────────────────┘

  Rollout data (obs, actions, rewards, dones)
       │
       ▼
  Compute advantages (GAE with γ=0.99*)
       │
       ▼
  For each mini-batch epoch:
       │
       ├── Compute policy ratio = π_new(a|s) / π_old(a|s)
       ├── Clip ratio to [0.85, 1.15]*  (ε=0.15*)
       ├── Policy loss = -min(ratio*A, clipped_ratio*A)
       ├── Value loss = (V(s) - return)²
       ├── Entropy bonus = 0.05* × H(π)
       ├── Total loss = policy + value - entropy
       └── Gradient step (clip grad norm ≤ 0.5*)

  * = fixed values (see rl_fix_verification.md for broken vs fixed)


 ┌─────────────────────────────────────────────────────────────┐
 │              WHERE BUGS BREAK LEARNING                      │
 └─────────────────────────────────────────────────────────────┘

  ┌─ Reward function ─────────────────────────────────────────┐
  │ • Wrong clip bounds → no negative feedback (Fix #1)       │
  │ • Wrong scales → alive dominates everything (Fix #2)      │
  │ • Wrong sigma → rewards too sparse to learn from          │
  │ IMPACT: Policy learns wrong behavior from step 1          │
  └───────────────────────────────────────────────────────────┘

  ┌─ PPO hyperparameters ─────────────────────────────────────┐
  │ • entropy_cost too low → premature convergence (Fix #3)   │
  │ • discount too low → myopic planning (Fix #4)             │
  │ • constant LR → can't escape local minima (Fix #5)        │
  │ IMPACT: Even correct rewards won't help if PPO is broken  │
  └───────────────────────────────────────────────────────────┘

  ┌─ Environment / sim ───────────────────────────────────────┐
  │ • Observation not normalized → unstable gradients         │
  │ • Action limits wrong → impossible poses                  │
  │ • Reference motions incomplete → gaps in imitation        │
  │ • No domain randomization → sim-only policy               │
  │ IMPACT: Policy works in sim, fails on hardware            │
  └───────────────────────────────────────────────────────────┘


 ┌─────────────────────────────────────────────────────────────┐
 │              PRE-LAUNCH CHECKLIST                            │
 └─────────────────────────────────────────────────────────────┘

  □ Training code cloned and present in repo
  □ All 5 fixes verified applied in actual source
  □ venv/Kaggle dependencies install clean
  □ env.reset() returns valid observation shape
  □ env.step() returns sane reward range (including negatives)
  □ 100K sanity run: entropy > 0.5, episodes > 20 steps
  □ 1M run: reward trending up, episode length increasing
  □ TensorBoard metrics match validation criteria
  □ Only THEN proceed to long training run
```
