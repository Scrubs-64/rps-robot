from game_engine.pickers.frequency_picker import FrequencyPicker
from game_engine.pickers.markov_picker import MarkovPicker
from game_engine.pickers.random_picker import RandomPicker


def make_picker(mode="random"):
    """Return a picker for the given mode name."""
    if mode == "random":
        return RandomPicker()
    if mode == "frequency":
        return FrequencyPicker()
    if mode == "adaptive":
        return MarkovPicker()
    raise ValueError(f"Unknown picker mode: {mode}")