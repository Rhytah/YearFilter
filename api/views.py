import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import PageYear

@api_view(['GET', 'POST'])
def year_filter(request):
    """
    API endpoint to filter page IDs by year.
    
    GET/POST Parameters:
    - page_ids: Comma-separated list of page IDs to filter (required)
    - year: Exact year to match (optional)
    - start_year: Start of year range (optional)
    - end_year: End of year range (optional)
    - simulated: If true, return simulated results (optional)
    
    Returns:
    JSON array of matching page IDs
    """
    # Handle both GET and POST requests
    params = request.query_params if request.method == 'GET' else request.data
    
    # Extract page_ids parameter
    page_ids_param = params.get('page_ids', '')
    if not page_ids_param:
        return Response(
            {"error": "page_ids parameter is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Parse page_ids
    try:
        page_ids = [int(pid.strip()) for pid in page_ids_param.split(',') if pid.strip()]
    except ValueError:
        return Response(
            {"error": "Invalid page_id format"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Extract other parameters
    year = params.get('year')
    start_year = params.get('start_year')
    end_year = params.get('end_year')
    simulated = params.get('simulated', '').lower() in ('true', '1', 't', 'yes')
    
    # Validate year parameters
    if year and (start_year or end_year):
        return Response(
            {"error": "Cannot specify both exact year and year range"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Handle simulation mode
    if simulated:
        return Response(
            simulate_results(page_ids, year, start_year, end_year)
        )
    
    # Process database query
    try:
        matching_page_ids = query_database(page_ids, year, start_year, end_year)
        return Response(matching_page_ids)
    except Exception as e:
        return Response(
            {"error": f"Database error: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def simulate_results(page_ids, year=None, start_year=None, end_year=None):
    """
    Generate simulated results for testing.
    
    Args:
        page_ids (list): List of page IDs to filter
        year (str): Exact year to match
        start_year (str): Start of year range
        end_year (str): End of year range
        
    Returns:
        list: Filtered list of page IDs
    """
    if not (year or (start_year and end_year)):
        # If no year filter is provided, return all page_ids
        return page_ids
    
    # Consistently seed random based on page_id to get deterministic results
    random.seed(sum(page_ids))
    
    # For simulation, randomly select approximately half of the pages
    return [pid for pid in page_ids if random.random() > 0.5]

def query_database(page_ids, year=None, start_year=None, end_year=None):
    """
    Query the database for matching page IDs.
    
    Args:
        page_ids (list): List of page IDs to filter
        year (str): Exact year to match
        start_year (str): Start of year range
        end_year (str): End of year range
        
    Returns:
        list: Filtered list of page IDs
    """
    # Start with all pages in the provided list
    query = Q(page_id__in=page_ids)
    
    # Apply year filters
    if year:
        query &= Q(year=int(year))
    elif start_year and end_year:
        query &= Q(year__gte=int(start_year)) & Q(year__lte=int(end_year))
    elif start_year:
        query &= Q(year__gte=int(start_year))
    elif end_year:
        query &= Q(year__lte=int(end_year))
    
    # Execute query and return only the page_ids as a list
    return list(PageYear.objects.filter(query).values_list('page_id', flat=True))