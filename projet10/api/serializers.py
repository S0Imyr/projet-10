from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type','author_user_id']
        read_only_fields = ['id', 'author_user_id']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project_id', 'status', 'author_user_id', 'assignee_user_id', 'created_time']
        read_only_fields = ['id', 'project_id', 'author_user_id', 'created_time']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user_id', 'issue_id', 'created_time']
        read_only_fields = ['id', 'author_user_id', 'issue_id']


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'project_id', 'permission', 'role']
        read_only_fields = ['project_id']

