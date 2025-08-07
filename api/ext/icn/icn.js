(function ICN9() {
  const targetURL = 'https://data.ssvd.online/3h.mp4';
  let hasPatched = false;
  let lastHref = location.href;
  let isFirstRun = true; // ✅ đánh dấu lần đầu

  console.log('[ICN9] Injected script loaded');
  unblockGoogleVideo(); // ✅ chỉ gọi 1 lần đầu

  function findTargetVideo() {
    return Array.from(document.querySelectorAll('video')).find(
      v => v.src && v.src !== targetURL
    );
  }

  function blockGoogleVideo() {
    chrome.runtime.sendMessage({ action: 'blockGoogleVideo' });
  }

  function unblockGoogleVideo() {
    chrome.runtime.sendMessage({ action: 'unblockGoogleVideo' });
  }

  function patchVideo(video) {
    try {
      const originalDuration = video.duration;
      video.src = targetURL;
      video.autoplay = true;

      Object.defineProperty(video, 'duration', {
        value: originalDuration,
        writable: true,
      });

      console.log('[ICN9] Replaced video.src');
      blockGoogleVideo();
      hasPatched = true;
    } catch (e) {
      console.warn('[ICN9] Patch error:', e);
    }
  }

  function schedulePatch(video) {
    if (!video || hasPatched) return;
    hasPatched = true;

    if (isFirstRun) {
      console.log('[ICN9] First video → Scheduling patch after 2s');
      isFirstRun = false;
      setTimeout(() => patchVideo(video), 2000);
    } else {
      console.log('[ICN9] New video → Patching immediately');
      patchVideo(video);
    }
  }

  function waitForVideoAndPatch() {
    const interval = setInterval(() => {
      const video = findTargetVideo();
      if (video) {
        clearInterval(interval);
        if (video.readyState >= 1) {
          schedulePatch(video);
        } else {
          video.addEventListener('loadedmetadata', () => {
            schedulePatch(video);
          }, { once: true });
        }
      }
    }, 300);
  }

  function monitorUrlChange() {
    setInterval(() => {
      if (location.href !== lastHref) {
        lastHref = location.href;
        hasPatched = false;

        console.log('[ICN9] URL changed → Looking for new video');
        unblockGoogleVideo();
        waitForVideoAndPatch(); // ✅ không delay
      }
    }, 1000);
  }

  function startICN9() {
    unblockGoogleVideo(); // ✅ unblock ngay đầu
    waitForVideoAndPatch(); // ✅ lần đầu delay sẽ xử lý bên trong
    monitorUrlChange();     // ✅ các lần sau không delay
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startICN9);
  } else {
    startICN9();
  }
})();
