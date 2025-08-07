// ICN9 Extension Bootstrap
console.log("Welcome ICN9");

// Configuration
const configs = {
  browser: "chrome",
  storageType: "local",
  contextMenuContexts: ["browser_action"],
  env: "prod",
  WEB_URL: "https://icn9.com",
  logLevel: "info"
};

// Expose to window
window.RQ = window.RQ || {};
window.RQ.configs = configs;

// Constants
const CONSTANTS = {
  PUBLIC_NAMESPACE: "__ICN9__",
  STRING_CONSTANTS: { SLASH: "" },
  LIMITS: {
    NUMBER_SHARED_LISTS: 10,
    NUMBER_EXECUTION_LOGS: 25
  },
  RULE_KEYS: {
    URL: "Url",
    HOST: "host",
    PATH: "path",
    HEADER: "Header",
    OVERWRITE: "Overwrite",
    IGNORE: "Ignore",
    PARAM: "param",
    VALUE: "value"
  },
  PATH_FROM_PAIR: {
    RULE_KEYS: "source.key",
    RULE_OPERATORS: "source.operator",
    SCRIPT_LIBRARIES: "libraries",
    SOURCE_PAGE_URL_OPERATOR: "source.filters.pageUrl.operator",
    SOURCE_PAGE_URL_VALUE: "source.filters.pageUrl.value",
    SOURCE_RESOURCE_TYPE: "source.filters.resourceType",
    SOURCE_REQUEST_METHOD: "source.filters.requestMethod",
    SOURCE_REQUEST_PAYLOAD_KEY: "source.filters.requestPayload.key",
    SOURCE_REQUEST_PAYLOAD_VALUE: "source.filters.requestPayload.value"
  },
  URL_COMPONENTS: {
    PROTOCOL: "Protocol",
    URL: "Url",
    HOST: "host",
    PATH: "path",
    QUERY: "query",
    HASH: "hash"
  },
  RULE_OPERATORS: {
    EQUALS: "Equals",
    CONTAINS: "Contains",
    MATCHES: "Matches",
    WILDCARD_MATCHES: "Wildcard_Matches"
  },
  CLIENT_MESSAGES: {
    GET_SCRIPT_RULES: "getScriptRules",
    DO_SETUP_RESPONSE_RULE_HANDLER: "doSetupResponseRuleHandler",
    GET_USER_AGENT_RULE_PAIRS: "getUserAgentRulePairs",
    OVERRIDE_RESPONSE: "overrideResponse",
    NOTIFY_RULES_APPLIED: "notifyRulesApplied",
    PRINT_CONSOLE_LOGS: "printConsoleLogs",
    GET_SESSION_RECORDING_CONFIG: "getSessionRecordingConfig",
    NOTIFY_SESSION_RECORDING_STARTED: "notifySessionRecordingStarted",
    IS_RECORDING_SESSION: "isRecordingSession",
    GET_TAB_SESSION: "getTabSession"
  },
  SCRIPT_TYPES: { URL: "url", CODE: "code" },
  SCRIPT_CODE_TYPES: { JS: "js", CSS: "css" },
  SCRIPT_LOAD_TIME: { BEFORE_PAGE_LOAD: "beforePageLoad", AFTER_PAGE_LOAD: "afterPageLoad" },
  SCRIPT_LIBRARIES: {
    JQUERY: { name: "jQuery", src: "https://code.jquery.com/jquery-2.2.4.js" },
    UNDERSCORE: { name: "Underscore", src: "https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js" }
  },
  RESPONSE_CODES: { NOT_FOUND: 404 },
  MESSAGES: {
    DELETE_ITEMS_NO_SELECTION_WARNING: "Please select one or more rules to delete.",
    DELETE_ITEMS: "Are you sure you want to delete the selected items?",
    DELETE_GROUP_WITH_RULES_WARNING: "There are some rules contained in this group. Please delete or ungroup them before deleting the group.",
    DELETE_GROUP: "Are you sure you want to delete the group?",
    UNGROUP_ITEMS_NO_SELECTION_WARNING: "Please select one or more rules to ungroup.",
    UNGROUP_ITEMS: "Are you sure you want to ungroup the selected items?",
    SIGN_IN_TO_VIEW_SHARED_LISTS: "Please login to view your Shared Lists.",
    SIGN_IN_TO_CREATE_SHARED_LISTS: "Please login to share the selected rules",
    SIGN_IN_TO_SUBMIT_QUERY: "Please login to contact our support team.",
    ERROR_AUTHENTICATION: "Received some error in authentication. Please try again later!!",
    SHARED_LISTS_LIMIT_REACHED: `You can not create more than ${10} shared lists`,
    ERROR_TAB_FOCUS: "The tab cannot be focused, as it might have been closed.",
    DEACTIVATE_REQUESTLY_MENU_OPTION: "Deactivate Requestly"
  },
  USER: {
    AUTHORIZED: "authorized-user",
    UNAUTHORIZED: "unauthorized-user"
  },
  getSharedListTimestamp: function (str) {
    return str.split("-")[0];
  }
};

// Attach constants
Object.assign(window.RQ, CONSTANTS);

// Inject main logic script once
(function injectScript() {
  const script = document.createElement("script");
  script.src = chrome.runtime.getURL("icn/injected.js");
  script.onload = () => script.remove();
  script.onerror = () => console.error("Failed to load injected.js");
  (document.head || document.documentElement).appendChild(script);
})();
