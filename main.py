from typing import Any
import httpx
import logging
import os
from mcp.server.fastmcp import FastMCP

class Config:
    """Custom configuration class for storing global settings."""
    uid: str = ""
    auth: str = ""
    device: str = ""
    log_file_path: str = ""

# Initialize configuration
config = Config()
config.uid = os.getenv("IQIYI_UID", "")
config.auth = os.getenv("IQIYI_AUTH", "")
config.device = os.getenv("IQIYI_DEVICE", "")

# Configure log directory and log file path
log_dir = os.getenv("IQIYI_LOG_DIR", "D:/temp/logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
config.log_file_path = os.getenv("IQIYI_LOG_FILE", os.path.join(log_dir, "mcp-server-iqiyi.log"))

# Configure logging with the custom log file path
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.log_file_path),
        logging.StreamHandler()  # Also print to console
    ]
)
logger = logging.getLogger('mcp-server-iqiyi')

logger.info("Starting iQiyi MCP server...")
# Initialize FastMCP server
mcp = FastMCP("iqiyi_video")

# Constants
IQIYI_API_BASE = "https://mesh.if.iqiyi.com/portal/lw/v7/channel/card/videoTab"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.iqiyi.com/"
}

# Add detailed logging to verify URL calls
async def make_iqiyi_request(params: dict, max_retries: int = 3) -> dict[str, Any] | None:
    """Make a request to the iQiyi API with proper error handling and retries."""
    async with httpx.AsyncClient() as client:
        last_error = None
        for attempt in range(max_retries):
            try:
                from urllib.parse import urlencode
                url = f"{IQIYI_API_BASE}?{urlencode(params)}"
                # logger.info(f"Attempting request to URL: {url}")  # Log the URL being called
                response = await client.get(
                    IQIYI_API_BASE,
                    params=params,
                    headers=DEFAULT_HEADERS,
                    timeout=60.0  # Increased timeout to 60 seconds
                )
                # logger.info(f"Response Ending! Status: {response.status_code}")  # Log the response status
                # response.raise_for_status()
                json_data = response.json()
                # logger.info(f"Full API Response: {json_data}")  # Log full response for debugging
                return json_data
            except Exception as e:
                last_error = e
                logger.error(f"Error making request to iQiyi API (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    import asyncio
                    await asyncio.sleep(2 * (attempt + 1))  # Exponential backoff
        logger.error(f"All {max_retries} attempts failed. Last error: {last_error}")
        return None

def format_video(video: dict) -> str:
    """Format a video item into a readable string."""
    return f"""
Title: {video.get('title', 'Unknown')}
Beirf: {video.get('desc', 'No description')}
PlayURL: {video.get('page_url', 'No URL')}
"""

@mcp.tool()
async def get_trending_videos(count: int = 10) -> str:
    """Get trending videos based on play count.
    
    Args:
        count: Number of videos to return (default 14)
    """
    params = {
        "channelName": "recommend",
        "play_record": "false",
        "img_size": "_284_160",
        "data_source": "v7_rec_sec_hot_rank_list",
        "tempId": "85",
        "data_id": "-1",
        "count": str(count),
        "block_id": "hot_ranklist",
        "showOrder": "1",
        "uid": config.uid,
        "vip": "0",
        "auth": config.auth,
        "device": config.device,
        "scale": "90",
        "brightness": "dark",
        "width": "690",
        "v": "13.034.21571",
        "conduit_id": "PPStream",
        "isLowPerformPC": "0",
        "os": "10.0.19044",
        "xcardParam": "",
        "from": "webapp"
    }
    
    response = await make_iqiyi_request(params)
    
    videos = []
    try:
        videos = response["items"][0].get("video", [])[0].get("data", [])
    except KeyError as e:
        logger.error(f"Response video list is empty: {e}")
    
    logger.info(f"Videos found: {len(videos)}")  # Log the number of videos found

    formatted_videos = [format_video(video) for video in videos[:count]]
    
    return "\n---\n".join(formatted_videos)

@mcp.tool()
async def get_new_releases(count: int = 10) -> str:
    """Get newly released videos.
    
    Args:
        count: Number of videos to return (default 14)
    """
    params = {
        "channelName": "recommend",
        "play_record": "false",
        "img_size": "_284_160",
        "data_source": "v7_hotspot_coming_data",
        "tempId": "85",
        "data_id": "303001",
        "count": str(count),
        "block_id": "hot_new",
        "uid": config.uid,
        "vip": "0",
        "auth": config.auth,
        "device": config.device,
        "scale": "90",
        "brightness": "dark",
        "width": "690",
        "v": "13.034.21571",
        "conduit_id": "PPStream",
        "isLowPerformPC": "0",
        "os": "10.0.19044",
        "xcardParam": "",
        "from": "webapp"
    }
    
    response = await make_iqiyi_request(params)
    
    videos = []
    try:
        videos = response["items"][0].get("video", [])[0].get("data", [])
    except KeyError as e:
        logger.error(f"Response video list is empty: {e}")
        
    formatted_videos = [format_video(video) for video in videos[:count]]
    return "\n---\n".join(formatted_videos)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
