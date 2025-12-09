"""
Project management pages for browsing, creating, and editing projects.
"""

from tcm.pages.projects.list import ProjectsListPage
from tcm.pages.projects.create import CreateProjectPage
from tcm.pages.projects.edit import EditProjectPage, NotFoundPage
from tcm.pages.projects.view import ViewProjectPage

__all__ = [
    "ProjectsListPage",
    "CreateProjectPage",
    "EditProjectPage",
    "ViewProjectPage",
    "NotFoundPage",
]
