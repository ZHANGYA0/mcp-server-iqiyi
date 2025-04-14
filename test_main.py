import asyncio
from main import make_iqiyi_request, get_trending_videos, get_new_releases

async def test_make_iqiyi_request():
    """Test the make_iqiyi_request function."""
    params = {
        "channelName": "recommend",
        "play_record": "false",
        "img_size": "_284_160",
        "data_source": "v7_rec_sec_hot_rank_list",
        "tempId": "85",
        "data_id": "-1",
        "count": "5",
        "block_id": "hot_ranklist",
        "showOrder": "1",
        "uid": "test_uid",
        "vip": "0",
        "auth": "test_auth",
        "device": "test_device",
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
    assert response is not None, "Request failed, response is None"
    assert "data" in response, "Response does not contain 'data'"
    print("Test passed: make_iqiyi_request works as expected.")

async def test_get_trending_videos():
    """Test the get_trending_videos function."""
    uid = "1737233463"
    auth = "c9XNaBhdUrUnPm2idSCBm28LCAnnUgwLKfckm1l6N0W98oN9qOlqm1WrrqCKVveTkrddOS5b"
    device = "6qylttx4h2unzx5lp3wt2umoyni6iy23"
    result = await get_trending_videos(uid, auth, device, count=5)
    assert result, "get_trending_videos returned an empty result"
    print("Test passed: get_trending_videos returned valid data.")
    print(result)

async def test_get_new_releases():
    """Test the get_new_releases function."""
    uid = "1737233463"
    auth = "c9XNaBhdUrUnPm2idSCBm28LCAnnUgwLKfckm1l6N0W98oN9qOlqm1WrrqCKVveTkrddOS5b"
    device = "6qylttx4h2unzx5lp3wt2umoyni6iy23"
    result = await get_new_releases(uid, auth, device, count=5)
    assert result, "get_new_releases returned an empty result"
    print("Test passed: get_new_releases returned valid data.")
    print(result)
# uid=1737233463
# auth=c9XNaBhdUrUnPm2idSCBm28LCAnnUgwLKfckm1l6N0W98oN9qOlqm1WrrqCKVveTkrddOS5b
# device=6qylttx4h2unzx5lp3wt2umoyni6iy23
if __name__ == "__main__":
    # asyncio.run(test_make_iqiyi_request())
    # asyncio.run(test_get_trending_videos())
    asyncio.run(test_get_new_releases())
