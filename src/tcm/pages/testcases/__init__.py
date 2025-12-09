"""
Test case pages for browsing and managing test cases.
"""

from tcm.pages.testcases.list import TestCasesListPage
from tcm.pages.testcases.create import CreateTestCasePage
from tcm.pages.testcases.edit import EditTestCasePage
from tcm.pages.testcases.view import ViewTestCasePage

__all__ = [
    "TestCasesListPage",
    "CreateTestCasePage",
    "EditTestCasePage",
    "ViewTestCasePage",
]
