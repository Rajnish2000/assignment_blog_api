
"""
blog views code here....
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from blog.serializers import BlogPostSerializer, BlogPostDetailSerializer
from core.models import BlogPost
from rest_framework.authentication import TokenAuthentication


class BlogPostViewSet(viewsets.ModelViewSet):
    """ View for managing blog posts """
    serializer_class = BlogPostDetailSerializer
    queryset = BlogPost.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Create a new blog post """
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """ Retrieve the blog posts for the authenticated user """
        return self.queryset.filter(
            author=self.request.user
        ).order_by('created_at')

    def get_serializer_class(self):
        """ Return the appropriate serializer class based on the action """
        if self.action == 'list':
            return BlogPostSerializer
        return self.serializer_class
