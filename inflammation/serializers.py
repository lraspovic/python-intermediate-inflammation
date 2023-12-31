import json
from abc import ABC
from inflammation import models

class Serializer(ABC):

    def serialize(self):
        pass

    def save(self):
        pass

    def deserialize(self):
        pass
    
    def load(self):
        pass
    
class ObservationSerializer(Serializer):
    model = models.Observation

    @classmethod
    def serialize(cls, instances):
        return [{
            'day': instance.day,
            'value': instance.value
        } for instance in instances]
    
    @classmethod
    def deserialize(cls, data):
        return [cls.model(**d) for d in data]


class PatientSerializer:
    model = models.Patient

    @classmethod
    def serialize(cls, instances):
       return [{
           'name' : instance.name,
           'observations': ObservationSerializer.serialize(instance.observations), 
       } for instance in instances
       ]
    
    @classmethod
    def deserialize(cls, data):
        instances = []

        for item in data:
            item['observations'] = ObservationSerializer.deserialize(item.pop('observations'))
            instances.append(cls.model(**item))
        
        return instances
    
class PatientJSONSerializer(PatientSerializer):
    @classmethod
    def save(cls, instances, path):
        with open(path, 'w') as jsonfile:
            json.dump(cls.serialize(instances), jsonfile)
    
    @classmethod
    def load(cls, path):
        with open(path) as jsonfile:
            data = json.load(jsonfile)
        
        return cls.deserialize(data)