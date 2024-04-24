
class CorpDefaults:
    class Defaults:
        def to_dict(self):
            # Improved method to get dictionary of properties
            return {attr: getattr(self, attr) for attr in dir(self) if
                    not attr.startswith("__") and not callable(getattr(self, attr)) and not isinstance(getattr(self, attr), staticmethod)}
    class IndustrialDefaults(Defaults):
        Polymer = 0
        Electronic_Parts = 0
        Scrap_Metal = 0
    class CriminalDefaults(Defaults):
        Weapons = 0
        Contraband = 0
        Surveillance_Gear = 0
    class LawDefaults(Defaults):
        Confidential_Files = 0
        Forensic_Equipment = 0
    @staticmethod
    def get_default_inventory(corp_type):
        if corp_type == "Industrial":
            return CorpDefaults.IndustrialDefaults()
        elif corp_type == "Criminal":
            return CorpDefaults.CriminalDefaults()
        elif corp_type == "Law":
            return CorpDefaults.LawDefaults()
        else:
            raise ValueError("Unknown corporation type")


