from collections import namedtuple
from gym import Env, spaces
import numpy as np
import copy

Location = namedtuple('Location', ['row', 'col'])
Action = namedtuple('Action', ['from_location', 'via_location', 'to_location'])

class Board:
    def __init__(self, state=None):
        if state is not None:
            self._state = copy.deepcopy(state)
        else:
            self._state = {}
            self.reset()

    def reset(self):
        new_state = copy.deepcopy(self._state)
        for location in LOCATIONS:
            new_state[location] = location != CENTRE
        return Board(new_state)

    @property
    def done(self):
        return not self.valid_actions()

    def valid_actions(self):
        action_indices = range(len(ACTIONS))
        return list(filter(self.is_valid_action, action_indices))

    def is_valid_action(self, action_index):
        assert 0 <= action_index < len(ACTIONS)
        action = ACTIONS[action_index]
        from_location, via_location, to_location = action
        assert from_location in LOCATIONS
        assert via_location in LOCATIONS
        assert to_location in LOCATIONS
        return all([
            self._state[from_location],
            self._state[via_location],
            not self._state[to_location]
        ])

    def make_move(self, action_index):
        assert 0 <= action_index < len(ACTIONS)
        action = ACTIONS[action_index]
        from_location, via_location, to_location = action
        assert from_location in LOCATIONS
        assert via_location in LOCATIONS
        assert to_location in LOCATIONS
        new_state = copy.deepcopy(self._state)
        assert new_state[from_location]
        assert new_state[via_location]
        assert not new_state[to_location]
        new_state[from_location] = False
        new_state[via_location] = False
        new_state[to_location] = True
        return Board(new_state)

    def __getitem__(self, location):
        return self._state[location]

    def __iter__(self):
        for item in self._state.items():
            yield item

    def __len__(self):
        return len(self._state)