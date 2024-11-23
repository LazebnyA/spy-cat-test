from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from spy_cat.models import SpyCat, Mission, Target
from config import VALID_BREEDS


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = "__all__"

    def validate_breed(self, value):
        if not any(breed.lower() == value.lower() for breed in VALID_BREEDS):
            raise serializers.ValidationError("Invalid breed.")
        return value


class TargetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Target
        fields = "__all__"


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = "__all__"

    def create(self, validated_data):
        targets_data = validated_data.pop("targets")
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission

    def update(self, instance, validated_data):
        targets_data = validated_data.pop("targets", [])
        instance.is_completed = validated_data.get("is_completed", instance.is_completed)

        for target_data in targets_data:
            target = Target.objects.get(id=target_data["id"], mission=instance)
            is_completed_target = target.is_completed
            for attr, value in target_data.items():
                if attr == "notes" and is_completed_target:
                    raise ValidationError(f"You cannot change notes, mission is already completed.")
                setattr(target, attr, value)
            target.save()

        instance.save()
        return instance
