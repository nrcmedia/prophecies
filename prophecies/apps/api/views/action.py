from pydoc import locate
from rest_framework import viewsets
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import PolymorphicResourceRelatedField
from actstream.models import Action
from django.contrib.auth.models import User
from prophecies.core.filters import ActionFilter
from prophecies.core.models import ActionAggregate, Choice, TaskRecord, TaskRecordReview, Tip


class GenericModelSerializer(serializers.ModelSerializer):
    MODEL_SERIALIZERS_MAPPING = {
        ActionAggregate: 'prophecies.apps.api.views.action_aggregate.ActionAggregateSerializer',
        User: 'prophecies.apps.api.views.user.UserSerializer',
        Choice: 'prophecies.apps.api.views.choice.ChoiceSerializer',
        TaskRecord: 'prophecies.apps.api.views.task_record.TaskRecordSerializer',
        Tip: 'prophecies.apps.api.views.tip.TipSerializer',
        TaskRecordReview: 'prophecies.apps.api.views.task_record_review.FlatTaskRecordReviewSerializer'
    }

    def get_instance_serializer(instance):
        instanceType = type(instance)
        serializer = GenericModelSerializer.MODEL_SERIALIZERS_MAPPING.get(instanceType, None)
        if type(serializer) == str:
            return locate(serializer)
        return serializer

    def __new__(self, instance=None, *args, **kwargs):
        if instance is not None:
            serializer = self.get_instance_serializer(instance)
            if serializer is not None:
                return serializer(instance, *args, **kwargs)
            self.Meta.model = type(instance)
        return super().__new__(self, instance, *args, **kwargs)

    class Meta:
        model = Action
        fields = ['id', 'url']


class ActionSerializer(serializers.HyperlinkedModelSerializer):
    actor = PolymorphicResourceRelatedField(GenericModelSerializer, many=False, read_only=True)
    action_object = PolymorphicResourceRelatedField(GenericModelSerializer, many=False, read_only=True)
    target = PolymorphicResourceRelatedField(GenericModelSerializer, many=False, read_only=True)

    included_serializers = {
        'actor': GenericModelSerializer,
        'action_object': GenericModelSerializer,
        'target': GenericModelSerializer
    }

    class Meta:
        model = Action
        resource_name = 'Action'
        fields = ['id', 'url', 'verb', 'actor', 'action_object', 'target',
                  'data', 'public', 'description', 'timestamp']

    class JSONAPIMeta:
        included_resources = ['actor', 'action_object', 'target']


class ActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    filterset_class = ActionFilter
    ordering = ['-timestamp']

    prefetch_for_includes = {
        'action': ['action', 'action__actor', 'action__target', 'action__action_object'],
        'action.actionObject': ['action', 'action__action_object']
    }
