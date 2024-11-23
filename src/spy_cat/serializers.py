from rest_framework import serializers

from spy_cat.models import SpyCat, Mission, Target


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = "__all__"


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        exclude = ("mission",)


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
            for attr, value in target_data.items():
                setattr(target, attr, value)
            target.save()

        instance.save()
        return instance
