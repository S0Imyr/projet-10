from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import get_object_or_404
from .models import Project, Contributor

class IsContributor(BasePermission):
    message = 'Only contributors are allowed'

    def has_permission(self, request, view):
        contributors = []
        if 'project_pk' in view.kwargs:
            project = get_object_or_404(Project, pk=view.kwargs['project_pk'])
            contributions = Contributor.objects.filter(project_id=project)
        for contribution in contributions:
            contributors.append(contribution.user_id)
        return  request.user in contributors
        

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            contributors = []
            contributions = Contributor.objects.filter(project_id=obj)
            for contribution in contributions:
                contributors.append(contribution.user_id)
            return  request.user in contributors
        else:
            return False

class IsAuthor(BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    """
    message = 'Only the author is allowed'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user_id == request.user
