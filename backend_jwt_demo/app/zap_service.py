# app/zap_service.py
import os, time
from typing import List, Dict
from zapv2 import ZAPv2

ZAP_API_KEY = os.getenv("ZAP_API_KEY", "27ad0vqks5210jlmqnnunpha9j")
ZAP_URL     = os.getenv("ZAP_URL", "http://127.0.0.1:8090")

# talk to ZAP via local proxy
zap = ZAPv2(
    apikey=ZAP_API_KEY,
    proxies={"http": ZAP_URL, "https": ZAP_URL},
)

def _wait_until(fn_status, id_value=None, label: str = "", timeout_s: int = 180, poll_s: float = 2.0):
    """
    Poll a ZAP status function until it returns '100' or timeout.
    """
    start = time.time()
    while True:
        try:
            status = fn_status(id_value) if id_value is not None else fn_status()
            pct = int(status)
        except Exception as e:
            raise RuntimeError(f"{label} status error: {e}")
        if pct >= 100:
            return
        if time.time() - start > timeout_s:
            raise TimeoutError(f"{label} timed out after {timeout_s}s (last={pct}%)")
        time.sleep(poll_s)

def run_zap_scan(target_url: str) -> List[Dict]:
    """
    Minimal, bounded scan for MVP:
    - Open URL (so it appears in Sites tree)
    - Spider with shallow limits
    - Active scan of target_url only (no recurse)
    - Return alerts for base URL
    """
    # Basic sanity
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "http://" + target_url

    try:
        # Make spider shallow & quick
        try:
            # these options may not exist on old ZAPs; ignore if they fail
            zap.spider.set_option_max_depth(2)
            zap.spider.set_option_max_children(10)
        except Exception:
            pass

        # Hit the page once so ZAP knows it
        zap.urlopen(target_url)
        time.sleep(2)

        # ---------- Spider ----------
        spider_id = zap.spider.scan(target_url, maxchildren=10)
        _wait_until(zap.spider.status, spider_id, label="Spider", timeout_s=120, poll_s=2)

        # Give passive scanner a moment
        time.sleep(2)

        # ---------- Active Scan ----------
        # keep it narrow & quick: recurse=False, inscopeOnly=False
        ascan_id = zap.ascan.scan(
            url=target_url, recurse=False, inScopeOnly=False
        )
        _wait_until(zap.ascan.status, ascan_id, label="Active Scan", timeout_s=180, poll_s=3)

        # ---------- Collect alerts ----------
        alerts = zap.core.alerts(baseurl=target_url) or []
        return alerts

    except TimeoutError as te:
        # propagate a clean error up so the router marks status=error
        raise RuntimeError(str(te)) from te
    except Exception as e:
        raise RuntimeError(f"ZAP scan failed: {e}") from e
