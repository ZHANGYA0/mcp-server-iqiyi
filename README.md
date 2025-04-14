# MCP Server for iQiYi

This project provides an MCP server implementation to access two iQiyi API endpoints:
1. **Get New Releases**: Fetches the latest released videos.
2. **Get Trending Videos**: Fetches the most popular videos.

The server is built using the `FastMCP` framework and exposes these functionalities as tools that can be accessed via the MCP protocol.

## Features

- **Get New Releases**: Returns a list of newly released videos with details such as title, description, image URL, and video URL.
- **Get Trending Videos**: Returns a list of trending videos with similar details.
- **Customizable Configuration**: Supports environment variables to configure user-specific parameters like `IQIYI_UID`, `IQIYI_AUTH`, and `IQIYI_DEVICE`.
- **Customizable Logging**: Allows specifying a custom log directory and log file path.

## Tools

### `get_new_releases`

Fetches the latest released videos.

**Inputs:**
- `count` (optional, integer): Number of videos to return (default: 14).

**Returns:** A formatted string containing details of the latest released videos.

---

### `get_trending_videos`

Fetches the most popular videos.

**Inputs:**
- `count` (optional, integer): Number of videos to return (default: 14).

**Returns:** A formatted string containing details of the trending videos.

---

## Configuration Example

Below is an example configuration for integrating this MCP server into your environment:

```json
{
  "mcpServers": {
    "mcp-server-iqiyi": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\myFile\\code\\mcp-server-iqiyi\\mcp-server-iqiyi",
        "run",
        "main.py"
      ],
      "autoApprove": [
        "get_new_releases",
        "get_trending_videos"
      ],
      "disabled": false,
      "timeout": 30,
      "env": {
        "IQIYI_UID": "<YOUR_UID>",
        "IQIYI_AUTH": "<YOUR_AUTH_TOKEN>",
        "IQIYI_DEVICE": "<YOUR_DEVICE_ID>",
        "IQIYI_LOG_DIR": "D:/custom/logs",  // Optional: Custom log directory
        "IQIYI_LOG_FILE": "D:/custom/logs/mcp-server-iqiyi.log"  // Optional: Custom log file path
      }
    }
  }
}
```

### Environment Variables

- `IQIYI_UID`: Your iQiyi user ID.
- `IQIYI_AUTH`: Authentication token for accessing the iQiyi API.
- `IQIYI_DEVICE`: Device identifier for the API request.
- `IQIYI_LOG_DIR` (Optional): Directory where logs will be stored. Defaults to `D:/temp/logs`.
- `IQIYI_LOG_FILE` (Optional): Full path to the log file. Defaults to `D:/temp/logs/mcp-server-iqiyi.log`.

## Usage

1. Clone the repository to your local machine.
2. Configure the MCP server settings as shown in the example above.
3. Start the MCP server using the configured command:
   ```bash
   uv --directory D:\myFile\code\mcp-server-iqiyi\mcp-server-iqiyi run main.py
   ```
4. Use the following tools:
   - `get_new_releases`: Fetches the latest released videos.
   - `get_trending_videos`: Fetches the most popular videos.

## Logging

Logs are stored in the directory specified by the `IQIYI_LOG_DIR` environment variable or the default directory `D:/temp/logs`. You can also specify a custom log file path using the `IQIYI_LOG_FILE` environment variable.

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
