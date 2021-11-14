"""
"""

from enum import Enum


class Accent(str, Enum):
    AU: str = "AU"
    CA: str = "CA"
    IE: str = "IE"
    IN: str = "IN"
    UK: str = "UK"
    US: str = "US"
    ZA: str = "ZA"

    @classmethod
    def tld_for(cls, region: str) -> str:
        return {
            "au": "com.au",
            "ca": "ca",
            "ie": "ie",
            "in": "co.in",
            "uk": "co.uk",
            "us": "com",
            "za": "co.za",
        }.get(region.lower())

    @property
    def tld(self) -> str:
        return self.tld_for(self.value)
