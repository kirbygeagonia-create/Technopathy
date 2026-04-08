from rest_framework import serializers
from .models import NavigationNode, NavigationEdge

class NavigationNodeSerializer(serializers.ModelSerializer):
    x_position = serializers.FloatField(source='x', read_only=True)
    y_position = serializers.FloatField(source='y', read_only=True)
    
    class Meta:
        model = NavigationNode
        fields = ['id', 'name', 'node_type', 'facility', 'room', 'map_svg_id', 
                  'x', 'y', 'x_position', 'y_position', 'floor', 'is_deleted', 
                  'created_at', 'updated_at']

class NavigationEdgeSerializer(serializers.ModelSerializer):
    from_node_name = serializers.CharField(source='from_node.name', read_only=True)
    to_node_name = serializers.CharField(source='to_node.name', read_only=True)
    from_node_id = serializers.IntegerField(source='from_node.id', read_only=True)
    to_node_id = serializers.IntegerField(source='to_node.id', read_only=True)
    
    class Meta:
        model = NavigationEdge
        fields = ['id', 'from_node', 'to_node', 'from_node_id', 'to_node_id', 
                  'from_node_name', 'to_node_name', 'distance', 'is_bidirectional', 
                  'is_deleted', 'created_at', 'updated_at']
