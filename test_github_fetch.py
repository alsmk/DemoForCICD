import unittest
from unittest.mock import patch, MagicMock
import fetch_info  # Import the main script
import requests

class TestGitHubFetch(unittest.TestCase):
    
    # Test for handling GitHub API responses correctly
    @patch('fetch_info.github_api_request')
    def test_fetch_latest_commit(self, mock_github_api_request):
        # Mock API response for the latest commit
        mock_github_api_request.return_value = [
            {
                'sha': 'abc123',
                'commit': {
                    'author': {'name': 'John Doe', 'date': '2021-09-01T12:34:56Z'},
                    'message': 'Initial commit'
                }
            }
        ]
        
        # Capture the printed output
        with patch('builtins.print') as mocked_print:
            fetch_info.fetch_latest_commit('owner/repo')
            mocked_print.assert_any_call("Latest Commit Details:")
            mocked_print.assert_any_call("Commit SHA: abc123")
            mocked_print.assert_any_call("Author: John Doe")
            mocked_print.assert_any_call("Message: Initial commit")
            mocked_print.assert_any_call("Date: 2021-09-01T12:34:56Z\n")
    
    # Test for network errors like timeouts
    @patch('requests.get')
    def test_network_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout
        with self.assertRaises(SystemExit):  # Expecting a system exit on error
            fetch_info.fetch_latest_commit('owner/repo')
    
    # Test for empty responses (no commits)
    @patch('fetch_info.github_api_request')
    def test_empty_commit_response(self, mock_github_api_request):
        mock_github_api_request.return_value = []
        with patch('builtins.print') as mocked_print:
            fetch_info.fetch_latest_commit('owner/repo')
            mocked_print.assert_any_call("Error: 404 - Not Found")

    # Test for fetching open issues with pagination
    @patch('fetch_info.github_api_request')
    def test_fetch_open_issues(self, mock_github_api_request):
        mock_github_api_request.side_effect = [
            # Page 1 response
            [
                {'title': 'Issue 1', 'state': 'open'},
                {'title': 'Issue 2', 'state': 'open'}
            ],
            # Empty page (end of pagination)
            []
        ]
        
        with patch('builtins.print') as mocked_print:
            fetch_info.fetch_open_issues('owner/repo')
            mocked_print.assert_any_call("Open Issues:")
            mocked_print.assert_any_call("Issue: Issue 1 (Status: open)")
            mocked_print.assert_any_call("Issue: Issue 2 (Status: open)")

    # Test for fetching pull requests with pagination
    @patch('fetch_info.github_api_request')
    def test_fetch_pull_requests(self, mock_github_api_request):
        mock_github_api_request.side_effect = [
            # Page 1 response
            [{'title': 'PR 1', 'state': 'open'}, {'title': 'PR 2', 'state': 'open'}],
            # Empty page (end of pagination)
            []
        ]
        
        with patch('builtins.print') as mocked_print:
            fetch_info.fetch_pull_requests('owner/repo')
            mocked_print.assert_any_call("Pull Requests:")
            mocked_print.assert_any_call("PR: PR 1 (Status: open)")
            mocked_print.assert_any_call("PR: PR 2 (Status: open)")

if __name__ == '__main__':
    unittest.main()
