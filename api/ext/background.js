chrome.runtime.onMessage.addListener((message) => {
  if (!chrome.declarativeNetRequest?.updateDynamicRules) {
    console.warn('[ICN9] DNR API not available in background');
    return;
  }

  switch (message.action) {
    case 'blockGoogleVideo':
      chrome.declarativeNetRequest.updateDynamicRules({
        addRules: [{
          id: 999,
          priority: 1,
          action: { type: 'block' },
          condition: {
            urlFilter: 'googlevideo.com/videoplayback',
            resourceTypes: ['media', 'xmlhttprequest', 'other']
          }
        }],
        removeRuleIds: []
      }, () => {
        if (chrome.runtime.lastError) {
          console.warn('[ICN9] Block error:', chrome.runtime.lastError.message);
        } else {
          console.log('[ICN9] Blocking googlevideo.com');
        }
      });
      break;

    case 'unblockGoogleVideo':
      chrome.declarativeNetRequest.updateDynamicRules({
        removeRuleIds: [999]
      }, () => {
        if (chrome.runtime.lastError) {
          console.warn('[ICN9] Unblock error:', chrome.runtime.lastError.message);
        } else {
          console.log('[ICN9] Unblocked googlevideo.com');
        }
      });
      break;
  }
});
