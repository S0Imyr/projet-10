from rest_framework.permissions import BasePermission, IsAdminUser


class IsContributor(BasePermission):
    message = 'Only contributors are allowed'

    def has_permission(self, request, view):
        contributors = []
        if 'pk' in view.kwargs:
            project = get_object_or_404(Project, pk=view.kwargs['pk'])
        elif 'pk1' in view.kwargs:
            project = get_object_or_404(Project, pk=view.kwargs['pk1'])
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
    message = 'Only the author is allowed'

    def has_permission(self, request, view):
        pass

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author_user_id
