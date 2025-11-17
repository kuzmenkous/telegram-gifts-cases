from dataclasses import asdict, dataclass


@dataclass
class BaseDTO:
    def dict(self) -> dict[str, str]:
        return {k: str(v) for k, v in asdict(self).items()}
