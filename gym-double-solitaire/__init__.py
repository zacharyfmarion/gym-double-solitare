from gym.envs.registration import register

register(
    id='gym-double-solitaire-v0',
    entry_point='gym_double_solitaire.envs:DoubleSolitaireEnv',
)