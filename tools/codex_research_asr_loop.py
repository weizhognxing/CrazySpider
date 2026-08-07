"""Resume Codex research ASR without overwriting raw results.

This script re-probes Douyin pages for fresh signed audio URLs and submits
short videos to Volc ASR. Every attempt writes new files under an attempt
directory; existing ASR JSON files are never modified or deleted.
"""

import argparse
import asyncio
import json
import os
import re
import time
import uuid
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright


SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
QUERY_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"
RESOURCE_ID = "volc.bigasr.auc"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def existing_success_ids(run_dir):
    ids = set()
    for path in Path(run_dir).glob("**/asr_result_*.json"):
        match = re.search(r"_(\d{18,})\.json$", path.name)
        if match:
            ids.add(match.group(1))
    return ids


def post_json(url, headers, payload, timeout=60):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return dict(response.headers), response.read().decode("utf-8", errors="replace")


def submit_asr(audio_url, app_id, token):
    task_id = str(uuid.uuid4())
    headers = {
        "X-Api-App-Key": app_id,
        "X-Api-Access-Key": token,
        "X-Api-Resource-Id": RESOURCE_ID,
        "X-Api-Request-Id": task_id,
        "X-Api-Sequence": "-1",
    }
    payload = {
        "user": {"uid": "opencode-codex-research"},
        "audio": {"format": "mp4", "url": audio_url},
        "request": {
            "model_name": "bigmodel",
            "language": "zh-CN",
            "enable_itn": True,
            "enable_punc": True,
            "show_utterances": True,
        },
    }
    try:
        headers_out, body = post_json(SUBMIT_URL, headers, payload)
        return {
            "ok": headers_out.get("X-Api-Status-Code") == "20000000",
            "task_id": task_id,
            "headers": headers_out,
            "body": body,
        }
    except Exception as exc:
        return {"ok": False, "task_id": task_id, "error": str(exc)}


def query_asr(task_id, app_id, token):
    headers = {
        "X-Api-App-Key": app_id,
        "X-Api-Access-Key": token,
        "X-Api-Resource-Id": RESOURCE_ID,
        "X-Api-Request-Id": task_id,
    }
    try:
        headers_out, body = post_json(QUERY_URL, headers, {})
        status = headers_out.get("X-Api-Status-Code")
        return {
            "ok": status == "20000000",
            "processing": status == "20000001",
            "headers": headers_out,
            "body": body,
        }
    except Exception as exc:
        return {"ok": False, "processing": False, "error": str(exc)}


async def reprobe_audio(page, video_id):
    media = []

    def on_response(response):
        url = response.url
        content_type = (response.headers.get("content-type") or "").lower()
        if "media-audio" in url or "media-video" in url or "audio" in content_type or "video" in content_type:
            media.append({"url": url, "status": response.status, "content_type": content_type})

    page.on("response", on_response)
    try:
        await page.goto(f"https://www.douyin.com/video/{video_id}", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(9000)
        try:
            await page.locator("video").first.click(timeout=2000)
            await page.wait_for_timeout(3000)
        except Exception:
            pass
        title = await page.title()
        body_text = await page.locator("body").inner_text(timeout=15000)
    finally:
        page.remove_listener("response", on_response)
    audio_url = next((item["url"] for item in media if "media-audio" in item["url"]), "")
    return {"title": title, "page_url": page.url, "body_text": body_text, "audio_url": audio_url, "media": media[-80:]}


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--max-seconds", type=int, default=900)
    parser.add_argument("--rounds", type=int, default=6)
    parser.add_argument("--sleep-between-rounds", type=int, default=60)
    parser.add_argument("--cdp", default="http://127.0.0.1:9223")
    args = parser.parse_args()

    app_id = os.environ.get("VOLC_ASR_APPID")
    token = os.environ.get("VOLC_ASR_TOKEN")
    if not app_id or not token:
        raise SystemExit("VOLC_ASR_APPID and VOLC_ASR_TOKEN are required")

    run_dir = Path(args.run_dir)
    summary = read_json(run_dir / "summary_progress.json")
    loop_root = run_dir / "asr_loop_attempts"
    loop_root.mkdir(exist_ok=True)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(args.cdp)
        context = browser.contexts[0]
        page = await context.new_page()

        for round_no in range(1, args.rounds + 1):
            success_ids = existing_success_ids(run_dir)
            targets = [
                item
                for item in summary
                if item["id"] not in success_ids
                and (item.get("duration_seconds") or 0) <= args.max_seconds
            ]
            attempt_dir = loop_root / f"round_{round_no:02d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            attempt_dir.mkdir(exist_ok=False)
            write_json(attempt_dir / "targets.json", targets)
            print(f"ROUND {round_no}: targets={len(targets)} success={len(success_ids)}")
            if not targets:
                break

            submitted = []
            for item in targets:
                index = item["index"]
                video_id = item["id"]
                print(f"PROBE {index:02d} {video_id}")
                probe = await reprobe_audio(page, video_id)
                write_json(attempt_dir / f"probe_{index:02d}_{video_id}.json", probe)
                if not probe.get("audio_url"):
                    write_json(attempt_dir / f"no_audio_{index:02d}_{video_id}.json", {"reason": "no_audio_url"})
                    continue
                result = submit_asr(probe["audio_url"], app_id, token)
                write_json(
                    attempt_dir / f"asr_submit_{index:02d}_{video_id}.json",
                    {key: value for key, value in result.items() if key != "body"},
                )
                if result.get("body"):
                    (attempt_dir / f"asr_submit_body_{index:02d}_{video_id}.json").write_text(
                        result["body"], encoding="utf-8"
                    )
                if result.get("ok"):
                    submitted.append({"index": index, "id": video_id, "task_id": result["task_id"]})
                print(f"SUBMIT {index:02d} ok={result.get('ok')} task={result.get('task_id')}")

            pending = {item["task_id"]: item for item in submitted}
            for poll_round in range(45):
                if not pending:
                    break
                time.sleep(4)
                for task_id in list(pending):
                    item = pending[task_id]
                    query = query_asr(task_id, app_id, token)
                    index = item["index"]
                    video_id = item["id"]
                    write_json(
                        attempt_dir / f"asr_query_meta_{index:02d}_{video_id}_r{poll_round:02d}.json",
                        {key: value for key, value in query.items() if key != "body"},
                    )
                    if query.get("ok"):
                        (attempt_dir / f"asr_result_{index:02d}_{video_id}.json").write_text(
                            query.get("body", ""), encoding="utf-8"
                        )
                        print(f"ASR_OK {index:02d} {video_id}")
                        del pending[task_id]
                    elif not query.get("processing"):
                        (attempt_dir / f"asr_failed_body_{index:02d}_{video_id}.json").write_text(
                            query.get("body", ""), encoding="utf-8"
                        )
                        print(f"ASR_FAIL {index:02d} {video_id}")
                        del pending[task_id]

            write_json(attempt_dir / "pending_after_poll.json", list(pending.values()))
            if round_no < args.rounds:
                time.sleep(args.sleep_between_rounds)

        await page.close()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
