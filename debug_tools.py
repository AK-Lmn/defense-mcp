import asyncio
from defense_mcp import get_defense_client
import logging
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


async def test_pagination_and_recent_threats():
    """Test pagination to see if we can find recent threats"""
    defense_client = await get_defense_client()
    
    try:
        first_page = await defense_client.get_threats()
        total_pages = first_page.get("total_pages", 1)
        total_count = first_page.get("total_count", 0)
        per_page = first_page.get("per_page", 25)
        
        logger.info(f"Pagination info: {total_pages} pages, {total_count} total threats, {per_page} per page")
        
        sample_pages = [1, 2, 3]
        if total_pages > 3:
            sample_pages.extend([total_pages - 2, total_pages - 1, total_pages])  # Last few pages
        
        sample_pages = list(set(sample_pages))  # Remove duplicates
        sample_pages = [p for p in sample_pages if 1 <= p <= total_pages]  # Valid pages only
        
        page_analysis = {}
        all_dates_found = []
        
        for page_num in sample_pages:
            try:
                page_response = await defense_client.client.get(
                    f"{defense_client.base_url}/v1/threats",
                    params={"page": page_num}
                )
                page_response.raise_for_status()
                page_data = page_response.json()
                
                threats = page_data.get("results", [])
                dates_on_page = [t.get("created_at") for t in threats if t.get("created_at")]
                all_dates_found.extend(dates_on_page)
                
                page_analysis[f"page_{page_num}"] = {
                    "threat_count": len(threats),
                    "date_range": {
                        "oldest": min(dates_on_page) if dates_on_page else None,
                        "newest": max(dates_on_page) if dates_on_page else None
                    },
                    "sample_dates": dates_on_page[:3] if dates_on_page else []
                }
                
            except Exception as e:
                page_analysis[f"page_{page_num}"] = {"error": str(e)}
        
        if all_dates_found:
            overall_oldest = min(all_dates_found)
            overall_newest = max(all_dates_found)
            
            from datetime import datetime, timedelta
            thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
            recent_dates = [d for d in all_dates_found if d >= thirty_days_ago]
        else:
            overall_oldest = overall_newest = None
            recent_dates = []
        
        last_page_threats = []
        if total_pages > 1:
            try:
                last_page_response = await defense_client.client.get(
                    f"{defense_client.base_url}/v1/threats",
                    params={"page": total_pages}
                )
                last_page_response.raise_for_status()
                last_page_data = last_page_response.json()
                last_page_threats = last_page_data.get("results", [])
            except Exception as e:
                logger.error(f"Failed to get last page: {e}")
        
        return {
            "pagination_info": {
                "total_pages": total_pages,
                "total_threats": total_count,
                "per_page": per_page,
                "estimated_total": total_pages * per_page
            },
            "page_analysis": page_analysis,
            "date_distribution": {
                "overall_oldest": overall_oldest,
                "overall_newest": overall_newest,
                "recent_threats_found": len(recent_dates),
                "sample_size": len(all_dates_found)
            },
            "last_page_sample": {
                "threat_count": len(last_page_threats),
                "sample_titles": [t.get("title") for t in last_page_threats[:3]],
                "sample_dates": [t.get("created_at") for t in last_page_threats[:3]]
            },
            "recommendations": [
                "If newest threats are on last pages, API sorts oldest-first",
                "Use full pagination to get recent threats",
                f"Consider fetching all {total_pages} pages to find today's threats"
            ]
        }
        
    except Exception as e:
        error_msg = f"Failed to test pagination: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}


async def debug_date_filtering():
    """Debug why date filtering is returning old threats"""
    defense_client = await get_defense_client()
    
    test_date = datetime.now() - timedelta(days=3)
    
    date_formats = {
        "iso_with_timezone": test_date.isoformat(),
        "iso_simple": test_date.strftime("%Y-%m-%dT%H:%M:%S"),
        "date_only": test_date.strftime("%Y-%m-%d"),
        "date_with_time": test_date.strftime("%Y-%m-%d %H:%M:%S"),
        "unix_timestamp": str(int(test_date.timestamp())),
    }
    
    results = {}
    
    for format_name, date_value in date_formats.items():
        try:
            params = {f"params[filter][after]": date_value}
            response = await defense_client.client.get(f"{defense_client.base_url}/v1/threats", params=params)
            response.raise_for_status()
            data = response.json()
            
            threats = data.get("results", [])
            if threats:
                threat_dates = []
                for threat in threats[:5]:
                    created_at = threat.get("created_at")
                    if created_at:
                        threat_dates.append(created_at)
                
                results[format_name] = {
                    "status": "success",
                    "total_threats": len(threats),
                    "sample_dates": threat_dates,
                    "oldest_threat": min(threat_dates) if threat_dates else None,
                    "newest_threat": max(threat_dates) if threat_dates else None,
                    "date_value_used": date_value
                }
            else:
                results[format_name] = {
                    "status": "success_no_results",
                    "total_threats": 0,
                    "date_value_used": date_value
                }
                
        except Exception as e:
            results[format_name] = {
                "status": "error",
                "error": str(e)[:200],
                "date_value_used": date_value
            }
    
    try:
        no_filter_response = await defense_client.client.get(f"{defense_client.base_url}/v1/threats")
        no_filter_response.raise_for_status()
        no_filter_data = no_filter_response.json()
        no_filter_threats = no_filter_data.get("results", [])
        
        if no_filter_threats:
            no_filter_dates = [t.get("created_at") for t in no_filter_threats[:10] if t.get("created_at")]
            results["no_filter_baseline"] = {
                "status": "success",
                "total_threats": len(no_filter_threats),
                "sample_dates": no_filter_dates,
                "oldest_in_sample": min(no_filter_dates) if no_filter_dates else None,
                "newest_in_sample": max(no_filter_dates) if no_filter_dates else None
            }
    except Exception as e:
        results["no_filter_baseline"] = {
            "status": "error",
            "error": str(e)[:200]
        }
    
    return {
        "message": "Date filtering debug results",
        "cutoff_date_requested": test_date.isoformat(),
        "current_date": datetime.now().isoformat(),
        "days_back": 3,
        "test_results": results,
        "analysis": {
            "working_formats": [k for k, v in results.items() if v.get("status") == "success"],
            "formats_with_no_results": [k for k, v in results.items() if v.get("status") == "success_no_results"],
            "failed_formats": [k for k, v in results.items() if v.get("status") == "error"]
        }
    }


async def test_date_filters(days: int = 1):
    """Test if date filters are working properly with the API"""
    from defense_mcp import get_date_range_filters
    
    defense_client = await get_defense_client()
    try:
        # Test without filters first
        logger.info("Testing API without date filters...")
        no_filter_response = await defense_client.get_threats(get_all_pages=False)
        total_without_filter = no_filter_response.get("total_count", 0)
        
        # Test with multiple different time ranges to verify filters work
        test_ranges = [1, 7, 30, 90]
        results = {}
        
        for test_days in test_ranges:
            logger.info(f"Testing API with date filters for last {test_days} days...")
            date_filters = get_date_range_filters(test_days)
            
            filtered_response = await defense_client.get_threats(date_filters, get_all_pages=False)
            total_with_filter = filtered_response.get("total_count", 0)
            
            results[f"{test_days}_days"] = {
                "count": total_with_filter,
                "filters_used": date_filters
            }
        
        counts = [results[f"{d}_days"]["count"] for d in test_ranges]
        filters_working = all(counts[i] <= counts[i+1] for i in range(len(counts)-1))
        
        return {
            "total_without_filter": total_without_filter,
            "filtered_results": results,
            "counts_progression": counts,
            "date_filters_working": filters_working,
            "diagnosis": "Date filters working - counts increase with longer time ranges" if filters_working else "Date filters may not be working - counts don't follow expected pattern"
        }
        
    except Exception as e:
        error_msg = f"Failed to test date filters: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}


if __name__ == "__main__":
    print("Running pagination test...")
    result = asyncio.run(test_pagination_and_recent_threats())
    print(f"Pagination test result: {result}")
    
    print("\nRunning debug date filtering...")
    debug_result = asyncio.run(debug_date_filtering())
    print(f"Debug date filtering result: {debug_result}")
    
    print("\nTesting current date filters...")
    date_filter_result = asyncio.run(test_date_filters())
    print(f"Date filter test result: {date_filter_result}")