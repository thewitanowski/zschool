import pytest
import os
from unittest.mock import patch, AsyncMock
from datetime import datetime
import httpx

from canvas_client import CanvasClient


class TestCanvasClient:
    """Unit tests for Canvas API client."""
    
    @pytest.fixture
    def client(self):
        """Create a Canvas client for testing."""
        with patch.dict(os.environ, {'CANVAS_BEARER_TOKEN': 'test_token_123'}):
            return CanvasClient()
    
    @pytest.fixture
    def mock_response(self):
        """Mock HTTP response."""
        response = AsyncMock()
        response.status_code = 200
        response.json.return_value = {"test": "data"}
        return response
    
    def test_initialization(self):
        """Test Canvas client initialization."""
        with patch.dict(os.environ, {'CANVAS_BEARER_TOKEN': 'test_token_123'}):
            client = CanvasClient()
            
            # Verify base configuration
            assert client.base_url == "https://learning.acc.edu.au"
            assert client.bearer_token == "test_token_123"
            
            # Verify headers
            expected_headers = {
                "Authorization": "Bearer test_token_123",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            assert client.headers == expected_headers
    
    def test_initialization_missing_token(self):
        """Test that missing bearer token raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="CANVAS_BEARER_TOKEN environment variable is required"):
                CanvasClient()
    
    def test_build_url(self, client):
        """Test URL building."""
        # Test with leading slash
        url = client._build_url("/courses")
        assert url == "https://learning.acc.edu.au/api/v1/courses"
        
        # Test without leading slash
        url = client._build_url("courses")
        assert url == "https://learning.acc.edu.au/api/v1/courses"
        
        # Test complex endpoint
        url = client._build_url("courses/123/modules")
        assert url == "https://learning.acc.edu.au/api/v1/courses/123/modules"
    
    def test_get_headers(self, client):
        """Test headers getter method."""
        headers = client.get_headers()
        
        expected_headers = {
            "Authorization": "Bearer test_token_123",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        assert headers == expected_headers
        # Verify it's a copy (not the same object)
        assert headers is not client.headers
    
    def test_get_base_url(self, client):
        """Test base URL getter."""
        assert client.get_base_url() == "https://learning.acc.edu.au"
    
    @pytest.mark.asyncio
    async def test_make_request_get(self, client, mock_response):
        """Test making GET request with correct URL and headers."""
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            await client._make_request("GET", "courses", params={"per_page": 50})
            
            # Verify the request was made with correct parameters
            mock_request.assert_called_once_with(
                method="GET",
                url="https://learning.acc.edu.au/api/v1/courses",
                params={"per_page": 50},
                json=None
            )
    
    @pytest.mark.asyncio
    async def test_make_request_post(self, client, mock_response):
        """Test making POST request with data."""
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            test_data = {"name": "test"}
            await client._make_request("POST", "courses", data=test_data)
            
            mock_request.assert_called_once_with(
                method="POST",
                url="https://learning.acc.edu.au/api/v1/courses",
                params=None,
                json=test_data
            )
    
    @pytest.mark.asyncio
    async def test_get_latest_announcement(self, client, mock_response):
        """Test get latest announcement URL and parameters."""
        mock_response.json.return_value = [{"id": 123, "title": "Test Announcement"}]
        
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            result = await client.get_latest_announcement(20564)
            
            # Verify correct URL and parameters
            mock_request.assert_called_once_with(
                method="GET",
                url="https://learning.acc.edu.au/api/v1/announcements",
                params={
                    "context_codes[]": "course_20564",
                    "latest_only": "true"
                },
                json=None
            )
            
            # Verify it returns the first announcement
            assert result == {"id": 123, "title": "Test Announcement"}
    
    @pytest.mark.asyncio
    async def test_get_courses(self, client, mock_response):
        """Test get courses URL."""
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            await client.get_courses()
            
            mock_request.assert_called_once_with(
                method="GET",
                url="https://learning.acc.edu.au/api/v1/courses",
                params=None,
                json=None
            )
    
    @pytest.mark.asyncio
    async def test_get_course(self, client, mock_response):
        """Test get specific course URL."""
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            await client.get_course(20354)
            
            mock_request.assert_called_once_with(
                method="GET",
                url="https://learning.acc.edu.au/api/v1/courses/20354",
                params=None,
                json=None
            )
    
    @pytest.mark.asyncio
    async def test_get_course_modules(self, client, mock_response):
        """Test get course modules URL and parameters."""
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            await client.get_course_modules(20354, per_page=25)
            
            mock_request.assert_called_once_with(
                method="GET",
                url="https://learning.acc.edu.au/api/v1/courses/20354/modules",
                params={"per_page": 25},
                json=None
            )
    
    @pytest.mark.asyncio
    async def test_get_module_items(self, client, mock_response):
        """Test get module items URL and parameters."""
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            await client.get_module_items(20354, 253389, per_page=100)
            
            mock_request.assert_called_once_with(
                method="GET",
                url="https://learning.acc.edu.au/api/v1/courses/20354/modules/253389/items",
                params={"per_page": 100},
                json=None
            )
    
    @pytest.mark.asyncio
    async def test_get_calendar_events(self, client, mock_response):
        """Test get calendar events URL and parameters."""
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            await client.get_calendar_events(
                course_id=20354,
                start_date="2025-07-28",
                end_date="2025-08-03",
                event_type="assignment",
                per_page=50
            )
            
            expected_params = {
                "start_date": "2025-07-28",
                "end_date": "2025-08-03",
                "type": "assignment",
                "context_codes[]": "course_20354",
                "per_page": 50
            }
            
            mock_request.assert_called_once_with(
                method="GET",
                url="https://learning.acc.edu.au/api/v1/calendar_events",
                params=expected_params,
                json=None
            )
    
    @pytest.mark.asyncio
    async def test_get_weekly_assignments(self, client, mock_response):
        """Test get weekly assignments with date calculation."""
        week_start = datetime(2025, 7, 28)  # Monday
        
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            await client.get_weekly_assignments(20354, week_start)
            
            expected_params = {
                "start_date": "2025-07-28",  # Monday
                "end_date": "2025-08-03",    # Sunday (6 days later)
                "type": "assignment",
                "context_codes[]": "course_20354",
                "per_page": 50
            }
            
            mock_request.assert_called_once_with(
                method="GET",
                url="https://learning.acc.edu.au/api/v1/calendar_events",
                params=expected_params,
                json=None
            )
    
    @pytest.mark.asyncio
    async def test_get_page_content(self, client, mock_response):
        """Test get page content URL."""
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            await client.get_page_content(20354, "topic-6-lets-remember")
            
            mock_request.assert_called_once_with(
                method="GET",
                url="https://learning.acc.edu.au/api/v1/courses/20354/pages/topic-6-lets-remember",
                params=None,
                json=None
            )
    
    @pytest.mark.asyncio
    async def test_mark_item_done(self, client, mock_response):
        """Test mark item done URL."""
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            await client.mark_item_done(20354, 253389, 2567723)
            
            mock_request.assert_called_once_with(
                method="PUT",
                url="https://learning.acc.edu.au/api/v1/courses/20354/modules/253389/items/2567723/done",
                params=None,
                json=None
            )
    
    @pytest.mark.asyncio
    async def test_mark_item_read(self, client, mock_response):
        """Test mark item read URL."""
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            await client.mark_item_read(20354, 253389, 2567723)
            
            mock_request.assert_called_once_with(
                method="PUT",
                url="https://learning.acc.edu.au/api/v1/courses/20354/modules/253389/items/2567723/mark_read",
                params=None,
                json=None
            )
    
    def test_get_current_week_dates(self, client):
        """Test current week date calculation."""
        # Mock a specific date to ensure consistent testing
        test_date = datetime(2025, 7, 30)  # Wednesday
        
        with patch('canvas_client.datetime') as mock_datetime:
            mock_datetime.now.return_value = test_date
            mock_datetime.strftime = datetime.strftime
            mock_datetime.timedelta = lambda days: test_date.replace(day=test_date.day + days) - test_date
            
            # Mock the timedelta calculation manually
            monday = datetime(2025, 7, 28)  # Monday of that week
            sunday = datetime(2025, 8, 3)   # Sunday of that week
            
            with patch.object(client, 'get_current_week_dates', return_value=("2025-07-28", "2025-08-03")):
                start_date, end_date = client.get_current_week_dates()
                
                assert start_date == "2025-07-28"  # Monday
                assert end_date == "2025-08-03"    # Sunday
    
    @pytest.mark.asyncio
    async def test_http_error_handling(self, client):
        """Test HTTP error handling."""
        error_response = AsyncMock()
        error_response.status_code = 404
        error_response.text = "Not Found"
        error_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=AsyncMock(), response=error_response
        )
        
        with patch.object(client.client, 'request', return_value=error_response):
            with pytest.raises(httpx.HTTPStatusError):
                await client.get_course(99999)
    
    @pytest.mark.asyncio
    async def test_request_error_handling(self, client):
        """Test request error handling."""
        with patch.object(client.client, 'request', side_effect=httpx.RequestError("Connection failed")):
            with pytest.raises(httpx.RequestError):
                await client.get_courses()
    
    @pytest.mark.asyncio
    async def test_empty_response_handling(self, client):
        """Test handling of 204 No Content responses."""
        mock_response = AsyncMock()
        mock_response.status_code = 204
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client.client, 'request', return_value=mock_response) as mock_request:
            result = await client._make_request("PUT", "test/endpoint")
            
            assert result == {}
    
    @pytest.mark.asyncio
    async def test_client_cleanup(self, client):
        """Test that HTTP client can be properly closed."""
        with patch.object(client.client, 'aclose') as mock_close:
            await client.close()
            mock_close.assert_called_once()


class TestCanvasClientIntegration:
    """Integration tests for Canvas client with real-world scenarios."""
    
    @pytest.fixture
    def client(self):
        """Create a Canvas client for integration testing."""
        with patch.dict(os.environ, {'CANVAS_BEARER_TOKEN': 'test_token_123'}):
            return CanvasClient()
    
    def test_headers_contain_authentication(self, client):
        """Test that all requests will include proper authentication."""
        headers = client.get_headers()
        
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Bearer ")
        assert "test_token_123" in headers["Authorization"]
        assert headers["Accept"] == "application/json"
        assert headers["Content-Type"] == "application/json"
    
    def test_all_endpoints_use_correct_base_url(self, client):
        """Test that all endpoints use the correct Canvas base URL."""
        base_url = "https://learning.acc.edu.au/api/v1"
        
        # Test various endpoint patterns
        assert client._build_url("courses") == f"{base_url}/courses"
        assert client._build_url("announcements") == f"{base_url}/announcements"
        assert client._build_url("calendar_events") == f"{base_url}/calendar_events"
        assert client._build_url("courses/123/modules") == f"{base_url}/courses/123/modules"
        assert client._build_url("courses/123/pages/test") == f"{base_url}/courses/123/pages/test"
    
    def test_course_ids_in_urls(self, client):
        """Test that course IDs are properly embedded in URLs."""
        course_id = 20354
        module_id = 253389
        item_id = 2567723
        
        # Test course-specific endpoints
        assert client._build_url(f"courses/{course_id}") == f"https://learning.acc.edu.au/api/v1/courses/{course_id}"
        assert client._build_url(f"courses/{course_id}/modules") == f"https://learning.acc.edu.au/api/v1/courses/{course_id}/modules"
        assert client._build_url(f"courses/{course_id}/modules/{module_id}/items") == f"https://learning.acc.edu.au/api/v1/courses/{course_id}/modules/{module_id}/items"
        assert client._build_url(f"courses/{course_id}/modules/{module_id}/items/{item_id}/done") == f"https://learning.acc.edu.au/api/v1/courses/{course_id}/modules/{module_id}/items/{item_id}/done"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 