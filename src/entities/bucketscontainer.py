from __future__ import annotations

from typing import Dict, Optional, ItemsView

from entities.bucket import Bucket, CompoundBucketList
from entities.serializable import Serializable, Deserializable
from serialization.store import DeserializationService



class BucketsContainer(Serializable, Deserializable):
    def __init__(self) -> None:
        super().__init__()
        self.bins: Dict[str, CompoundBucketList] = {}

    def items(self) -> ItemsView[str, CompoundBucketList]:
        return self.bins.items()

    def add(self, indicator: str, value: CompoundBucketList):
        self.bins[indicator] = value

    def get(self, indicator: str) -> Optional[CompoundBucketList]:
        return self.bins[indicator] if indicator in self.bins else None

    def serialize(self) -> Dict:
        data = super().serialize()
        for key, value in self.bins.items():
            if isinstance(value[0], list):
                data[key] = [[x.serialize() for x in arr] for arr in value]
            elif isinstance(value[0], Bucket):
                data[key] = [x.serialize() for x in value]

        return data

    @classmethod
    def deserialize(cls, data: Dict) -> BucketsContainer:
        bins = BucketsContainer()
        for key, value in data.items():
            if key == '__class__':
                continue

            if isinstance(value[0], list):
                lists = [[DeserializationService.deserialize(x) for x in lst] for lst in value]
                bins.add(key, lists)
            else:
                bins.add(key, [DeserializationService.deserialize(x) for x in value])

        return bins


BucketsContainer()