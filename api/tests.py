from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import PageYear

class YearFilterTests(TestCase):
    """
    Test cases for the year filter API.
    """
    
    def setUp(self):
        """Set up test data."""
        # Create test data
        self.page_years = [
            PageYear.objects.create(page_id=101, year=1990),
            PageYear.objects.create(page_id=102, year=1995),
            PageYear.objects.create(page_id=103, year=2000),
            PageYear.objects.create(page_id=104, year=2005),
            PageYear.objects.create(page_id=105, year=2010),
        ]
        self.client = APIClient()
        
    def test_filter_by_exact_year(self):
        """Test filtering by exact year."""
        # Test with year=1995
        response = self.client.get(
            reverse('year_filter'), 
            {'page_ids': '101,102,103,104,105', 'year': '1995'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [102])
        
    def test_filter_by_year_range(self):
        """Test filtering by year range."""
        # Test with start_year=1995, end_year=2005
        response = self.client.get(
            reverse('year_filter'), 
            {'page_ids': '101,102,103,104,105', 'start_year': '1995', 'end_year': '2005'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.json()), {102, 103, 104})
        
    def test_filter_with_invalid_parameters(self):
        """Test with invalid parameters."""
        # Test without page_ids
        response = self.client.get(
            reverse('year_filter'), 
            {'year': '1995'}
        )
        self.assertEqual(response.status_code, 400)
        
        # Test with both exact year and year range
        response = self.client.get(
            reverse('year_filter'), 
            {'page_ids': '101,102,103', 'year': '1995', 'start_year': '1990'}
        )
        self.assertEqual(response.status_code, 400)
        
    def test_simulation_mode(self):
        """Test simulation mode."""
        # Since simulation uses random, test that response is a list of integers
        response = self.client.get(
            reverse('year_filter'), 
            {'page_ids': '101,102,103,104,105', 'year': '2000', 'simulated': 'true'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))
        for item in response.json():
            self.assertTrue(isinstance(item, int))
            
    def test_post_request(self):
        """Test POST request."""
        # Test with POST method
        response = self.client.post(
            reverse('year_filter'), 
            {'page_ids': '101,102,103,104,105', 'year': '1995'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [102])