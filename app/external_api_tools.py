# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import urllib.request
import json

logger = logging.getLogger(__name__)


def get_github_repo_details(owner: str = "google", repo: str = "adk") -> dict:
    """Fetch live repository statistics, stars, description, open issues, and primary language from the GitHub Public API.

    Args:
        owner: GitHub repository owner or organization (default: 'google').
        repo: GitHub repository name (default: 'adk').

    Returns:
        Dictionary containing real repository metadata and statistics.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    logger.info(f"Calling GitHub API: {url}")
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Tribal-KT-Agent-Client/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "name": data.get("full_name"),
                "description": data.get("description"),
                "stars": data.get("stargazers_count"),
                "forks": data.get("forks_count"),
                "open_issues": data.get("open_issues_count"),
                "language": data.get("language"),
                "license": data.get("license", {}).get("spdx_id") if data.get("license") else "N/A",
                "html_url": data.get("html_url"),
            }
    except Exception as e:
        logger.error(f"Error fetching GitHub repo details: {str(e)}")
        return {"error": f"Failed to fetch GitHub repo details: {str(e)}"}


def get_team_location_weather_and_time(city: str = "New York") -> dict:
    """Fetch live weather and current climate metrics for team member locations using the Open-Meteo free API.

    Args:
        city: City name where team members or offices are located (e.g. 'New York', 'San Francisco', 'London', 'Tokyo').

    Returns:
        Dictionary containing real live weather metrics.
    """
    city_coords = {
        "new york": (40.7128, -74.0060),
        "san francisco": (37.7749, -122.4194),
        "london": (51.5074, -0.1278),
        "tokyo": (35.6762, 139.6503),
        "seattle": (47.6062, -122.3321),
    }

    lat, lon = city_coords.get(city.lower().strip(), (40.7128, -74.0060))
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    logger.info(f"Calling Open-Meteo API for {city}: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Tribal-KT-Agent-Client/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            curr = data.get("current_weather", {})
            return {
                "city": city.title(),
                "temperature_celsius": curr.get("temperature"),
                "windspeed_kmh": curr.get("windspeed"),
                "is_day": "Day" if curr.get("is_day") == 1 else "Night",
                "latitude": lat,
                "longitude": lon,
            }
    except Exception as e:
        logger.error(f"Error fetching weather for {city}: {str(e)}")
        return {"error": f"Failed to fetch weather: {str(e)}"}
