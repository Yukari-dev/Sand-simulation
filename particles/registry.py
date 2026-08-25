from particles.elements import Sand, Stone, Wood, Water, Fire, Smoke


class ElementRegistry:
    _elements = {
        "Sand": Sand,
        "Stone": Stone,
        "Wood": Wood,
        "Water": Water,
        "Fire": Fire,
        "Smoke": Smoke,
    }

    @classmethod
    def get(cls, name):
        return cls._elements.get(name, "Sand")

    @classmethod
    def list_all(cls):
        return list(cls._elements.keys())
