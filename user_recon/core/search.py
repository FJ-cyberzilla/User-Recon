import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from user_recon.utils.logging import get_logger
from user_recon.core.security import sanitize_input
from user_recon.utils.retry_queue import enqueue_retry

logger = get_logger(__name__)

# Social media and communication platforms
SITES = {
    "YouTube": "https://www.youtube.com/{user}",
    "Reddit": "https://www.reddit.com/user/{user}",
    "Facebook": "https://www.facebook.com/{user}",
    "Twitter": "https://www.twitter.com/{user}",
    "Twitch": "https://www.twitch.tv/{user}",
    "GitHub": "https://www.github.com/{user}",
    "Instagram": "https://www.instagram.com/{user}",
    "Pinterest": "https://www.pinterest.com/{user}",
    "Roblox": "https://www.roblox.com/user.aspx?username={user}",
    "Bluesky": "https://bsky.app/profile/{user}.bsky.social",
    "Sanista": "https://www.sanista.com/{user}",  # placeholder, update if real pattern differs
    "Telegram": "https://t.me/{user}",
    "WeChat": "https://www.wechat.com/{user}",    # placeholder, WeChat doesn’t expose usernames publicly
    "WhatsApp": "https://wa.me/{user}",           # requires phone number in international format
    "Signal": "https://signal.me/#p/{user}",      # requires phone number, may not resolve for all users
    "Microsoft Teams": "https://teams.microsoft.com/l/profile/{user}",
    "TikTok": "https://www.tiktok.com/@{user}",
    "LinkedIn": "https://www.linkedin.com/in/{user}",
    "Medium": "https://medium.com/@{user}",
    "Imgur": "https://imgur.com/user/{user}",
    "Vimeo": "https://vimeo.com/{user}",
    "Spotify": "https://open.spotify.com/user/{user}",
    "Keybase": "https://keybase.io/{user}",
    "Snapchat": "https://www.snapchat.com/add/{user}",
    "SoundCloud": "https://soundcloud.com/{user}",
    "VK": "https://vk.com/{user}",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (UserRecon/1.0; +https://github.com/your-org/user-recon)"
}


def check_username(username: str, site: str) -> dict:
    """
    Check if a username exists on a given site.
    Returns dict with status and reasoning.
    """
    username = sanitize_input(username)
    url = SITES[site].format(user=username)

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        status = resp.status_code

        if status == 200:
            return {"site": site, "url": url, "found": True, "status": status}
        elif status in (301, 302):
            return {"site": site, "url": url, "found": True, "status": status}
        elif status == 404:
            return {"site": site, "url": url, "found": False, "status": status}
        elif status == 403:
            return {"site": site, "url": url, "found": None, "status": status, "error": "Forbidden"}
        elif status == 429:
            enqueue_retry(username, site)
            return {"site": site, "url": url, "found": None, "status": status, "error": "Rate limited"}
        elif status == 999:
            enqueue_retry(username, site)
            return {"site": site, "url": url, "found": None, "status": status, "error": "Blocked by platform"}
        else:
            enqueue_retry(username, site)
            return {"site": site, "url": url, "found": None, "status": status, "error": "Unhandled response"}

    except (Timeout, ConnectionError):
        enqueue_retry(username, site)
        return {"site": site, "url": url, "found": None, "error": "Network error, queued for retry"}
    except RequestException as e:
        enqueue_retry(username, site)
        return {"site": site, "url": url, "found": None, "error": f"Request failed: {e}"}


def check_all_sites(username: str) -> list:
    """
    Run username check across all platforms.
    Returns list of result dicts.
    """
    results = []
    for site in SITES.keys():
        result = check_username(username, site)
        results.append(result)
        logger.info(f"[{site}] {result}")
    return results
