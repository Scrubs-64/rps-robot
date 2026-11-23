class MockArm:
    """Fake arm for testing without hardware. Just prints what it would do."""

    def ready(self):
        print("[arm] ready pose")

    def pump(self):
        print("[arm] pump x3")

    def show(self, move):
        print(f"[arm] shows {move}")

    def stop(self):
        print("[arm] STOP")
