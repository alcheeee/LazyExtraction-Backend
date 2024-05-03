from enum import Enum
from pydantic import BaseModel

class CorporationType(str, Enum):
    Industrial = "Industrial"
    Criminal = "Criminal"
    Law = "Law"

class NewCorporationInfo(BaseModel):
    name: str
    type: CorporationType

class ItemType(Enum):
    POLYMER = "Polymer"
    ELECTRONIC_PARTS = "Electronic Parts"
    SCRAP_METAL = "Scrap Metal"
    WEAPONS = "Weapons"
    CONTRABAND = "Contraband"
    SURVEILLANCE_GEAR = "Surveillance Gear"
    CONFIDENTIAL_FILES = "Confidential Files"
    FORENSIC_EQUIPMENT = "Forensic Equipment"

class UpgradeType(Enum):
    INDUSTRIAL_PRODUCTION = "Production Efficiency"
    INDUSTRIAL_LEVEL = "Production Capability"
    CRIMINAL_NETWORKS = "Criminal Networks"
    CRIMINAL_MONEY_LAUNDERING = "Money Laundering"
    LAW_FORENSICS = "Forensics"
    LAW_LEGAL_FRAMEWORKS = "Legal Frameworks"

class CorporationDefaults:
    DEFAULTS = {
        CorporationType.Industrial: {
            'items': [ItemType.POLYMER, ItemType.ELECTRONIC_PARTS, ItemType.SCRAP_METAL],
            'upgrades': [UpgradeType.INDUSTRIAL_PRODUCTION, UpgradeType.INDUSTRIAL_LEVEL]
        },
        CorporationType.Criminal: {
            'items': [ItemType.WEAPONS, ItemType.CONTRABAND, ItemType.SURVEILLANCE_GEAR],
            'upgrades': [UpgradeType.CRIMINAL_NETWORKS, UpgradeType.CRIMINAL_MONEY_LAUNDERING]
        },
        CorporationType.Law: {
            'items': [ItemType.CONFIDENTIAL_FILES, ItemType.FORENSIC_EQUIPMENT],
            'upgrades': [UpgradeType.LAW_FORENSICS, UpgradeType.LAW_LEGAL_FRAMEWORKS]
        }
    }

    @staticmethod
    def get_defaults(corp_type: CorporationType):
        return CorporationDefaults.DEFAULTS.get(corp_type, {'items': [], 'upgrades': []})