from django.db import models
from django.conf import settings


CONTRIBUTOR_PERMISSION_CHOICES = (('not allowed','not allowed'), ('allowed','allowed'))
PROJECT_TYPE_CHOICES = (('back-end','back-end'), ('front-end', 'front-end'), ('iOS','iOS') , ('Android','Android'))
ISSUE_PRIORITY_CHOICES = (('low', 'low'), ('medium', 'medium'), ('high', 'high'))
ISSUE_TAG_CHOICES = (('bug', 'bug'), ('upgrade', 'upgrade'), ('task', 'task'))
ISSUE_STATUS_CHOICES = (('to do', 'to do'), ('in progress', 'in progress'), ('finished', 'finished'))


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=8192)
    type = models.CharField(max_length=128, choices=PROJECT_TYPE_CHOICES)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.title


class Contributor(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=128, choices=CONTRIBUTOR_PERMISSION_CHOICES)
    role = models.CharField(max_length=128)

    class Meta:
        unique_together = ('user_id', 'project_id', )

    def __str__(self):
        return f"{self.user_id} work on {self.project_id}"


class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=8192)
    tag = models.CharField(max_length=128, choices=ISSUE_TAG_CHOICES)
    priority = models.CharField(max_length=128, choices=ISSUE_PRIORITY_CHOICES)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=128, choices=ISSUE_STATUS_CHOICES)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="Written_by")
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="Assign_to")
    created_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Project: {self.project_id} - {self.title}"


class Comment(models.Model):
    description = models.CharField(max_length=8192)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Issue {self.issue_id} - comment {self.id}"
