# Changelog

## Unreleased (next release, from the API's public document of 2026-11-15)

The API's public document was cleaned up. Regenerating this SDK from it
brings these changes; plan them as a breaking release.

### Renamed API classes

The API groups its endpoints in sections, and each section is one API class.
Five sections were renamed so a developer finds them, which renames their
class (the methods keep their names):

| Before | After |
|---|---|
| AllowancesApi | PlanUsageApi |
| AnalyticsDataApi and WorkspaceMetricsApi | AnalyticsApi (merged) |
| AnalyticsDashboardApi | AnalyticsDashboardsApi |
| ContactIntegrationsApi | IntegrationsContactToolsApi |
| FormIntegrationsApi | IntegrationsFormsApi |
| GoogleFormsIntegrationsApi | IntegrationsGoogleFormsApi |
| SlackIntegrationsApi | IntegrationsSlackApi |
| GoogleAnalyticsIntegrationsApi | IntegrationsGoogleAnalyticsApi |
| RetargetingPixelsApi | IntegrationsRetargetingPixelsApi |

(Class names are shown in PascalCase; each language keeps its own casing and
file naming, e.g. plan_usage_api.py.)

### Removed operations

These were never usable with an API token (they need a dashboard session, or
finish a browser sign-in), or were superseded. They are no longer in the
public API, so their methods go away:

- AssistantApi, AgentIdentityApi, ReviewRewardsApi, TimeSeriesApi and
  IntegrationsServiceApi entirely;
- MembersApi: getMyself, updateMyself, listMyWorkspaces, createMyWorkspace,
  switchWorkspace;
- PlanUsageApi (was AllowancesApi): dismissAllowanceNotice;
- WorkspacesApi: getWorkspace (use getMyWorkspace), updateOriginInquiry,
  updateOriginPurpose, requestEnrollment;
- the integration classes: the OAuth sign-in start and completion methods
  (startOAuth, completeOAuth, getOAuthURL);
- LinksApi: resolveQrcodeImages; QrCodeTemplatesApi:
  resolveQrcodeTemplateImages; PageThemeTemplatesApi:
  resolvePageThemeTemplateImages, findMatchingPageThemeTemplate;
- AnalyticsApi (was WorkspaceMetricsApi): getWorkspaceInsight;
- CustomDomainsApi: validationInstructions (use getSetupGuide).

### Other

- POST /v1/links/batch has its own summary, distinct from /v1/links/bulk.
- ErrorResponse.code is documented as the gRPC status code (16 for missing
  credentials), which is what the API has always returned.
