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

### Renamed operations (contract rename of 2026-11-15)

The API renamed its services and operations so the contract reads the way
it works (decision of 2026-11-15). Method names come from the operation ids,
so these methods are renamed (shown as operation ids; each language keeps its
own casing, e.g. `PlanUsageService_List` is `plan_usage_service_list` in
Python and Rust, `planUsageServiceList` in TypeScript and Java and
`PlanUsageServiceList` in Go):

| Before | After |
|---|---|
| AllowancesService_ListAllowances | PlanUsageService_List |
| AnalyticsDashboardService_CreateDashboard | AnalyticsDashboardsService_Create |
| AnalyticsDashboardService_DeleteDashboard | AnalyticsDashboardsService_Delete |
| AnalyticsDashboardService_GenerateWidgetSummary | AnalyticsDashboardsService_GenerateWidgetSummary |
| AnalyticsDashboardService_GetWidgetSummary | AnalyticsDashboardsService_GetWidgetSummary |
| AnalyticsDashboardService_ListDashboards | AnalyticsDashboardsService_List |
| AnalyticsDashboardService_UpdateDashboard | AnalyticsDashboardsService_Update |
| AnalyticsDataService_GetAttributeDistribution | AnalyticsService_GetAttributeDistribution |
| AnalyticsDataService_GetAttributeMetric | AnalyticsService_GetAttributeMetric |
| AnalyticsDataService_GetAttributeValues | AnalyticsService_GetAttributeValues |
| AnalyticsDataService_GetBreakdown | AnalyticsService_GetBreakdown |
| AnalyticsDataService_GetDeviceDistribution | AnalyticsService_GetDeviceDistribution |
| AnalyticsDataService_GetGeoBreakdown | AnalyticsService_GetGeoBreakdown |
| AnalyticsDataService_GetGroupedTimeSeries | AnalyticsService_GetGroupedTimeSeries |
| AnalyticsDataService_GetHourOfDayDistribution | AnalyticsService_GetHourOfDayDistribution |
| AnalyticsDataService_GetSharedLocations | AnalyticsService_GetSharedLocations |
| AnalyticsDataService_GetStepFunnel | AnalyticsService_GetStepFunnel |
| AnalyticsDataService_GetTopLinks | AnalyticsService_GetTopLinks |
| AnalyticsDataService_GetTrafficSplitResults | AnalyticsService_GetTrafficSplitResults |
| AnalyticsDataService_GetVisitorTrends | AnalyticsService_GetVisitorTrends |
| AnalyticsDataService_ListVisitorCountries | AnalyticsService_ListVisitorCountries |
| CustomDomainsService_Check | CustomDomainsService_Verify |
| EventsService_ListEventTraces | EventsService_ListTraces |
| EventsService_ListEvents | EventsService_List |
| LinksService_ShortlinkAvailability | LinksService_CheckShortlinkAvailability |
| LinksService_ShortlinkRandom | LinksService_GenerateShortlink |
| MetricsService_GetEventsMetric | AnalyticsService_GetEventsMetric |
| MetricsService_GetWorkspaceMetric | AnalyticsService_GetWorkspaceMetric |
| PageThemeTemplatesService_CreatePageThemeTemplate | PageThemeTemplatesService_Create |
| PageThemeTemplatesService_DeletePageThemeTemplate | PageThemeTemplatesService_Delete |
| PageThemeTemplatesService_GetPageThemeTemplate | PageThemeTemplatesService_Get |
| PageThemeTemplatesService_ImportPageThemeTemplate | PageThemeTemplatesService_Import |
| PageThemeTemplatesService_ListPageThemeTemplates | PageThemeTemplatesService_List |
| PageThemeTemplatesService_PublicGetPageThemeTemplate | PageThemeTemplatesService_GetPublic |
| PageThemeTemplatesService_PublicListPageThemeTemplates | PageThemeTemplatesService_ListPublic |
| PageThemeTemplatesService_PublishPageThemeTemplate | PageThemeTemplatesService_Publish |
| PageThemeTemplatesService_UpdatePageThemeTemplate | PageThemeTemplatesService_Update |
| PageThemeTemplatesService_UpdatePageThemeTemplateStyling | PageThemeTemplatesService_UpdateStyling |
| PageThemesService_ApplyPageThemeTemplate | PageThemesService_ApplyTemplate |
| PageThemesService_BulkUpdatePageThemes | PageThemesService_BulkUpdate |
| PageThemesService_GetPageTheme | PageThemesService_Get |
| PageThemesService_ListPageThemes | PageThemesService_List |
| PageThemesService_UpdatePageTheme | PageThemesService_Update |
| PricingService_ListPricingPlans | PricingService_ListPlans |
| QrcodeDesignService_ApplyTemplate | QrcodeDesignsService_ApplyTemplate |
| QrcodeDesignService_Delete | QrcodeDesignsService_Delete |
| QrcodeDesignService_Get | QrcodeDesignsService_Get |
| QrcodeDesignService_PublicCreate | QrcodeDesignsService_Create |
| QrcodeDesignService_Update | QrcodeDesignsService_Update |
| QrcodeTemplatesService_CreateQrcodeTemplate | QrcodeTemplatesService_Create |
| QrcodeTemplatesService_DeleteQrcodeTemplate | QrcodeTemplatesService_Delete |
| QrcodeTemplatesService_GetQrcodeTemplate | QrcodeTemplatesService_Get |
| QrcodeTemplatesService_ImportQrcodeTemplate | QrcodeTemplatesService_Import |
| QrcodeTemplatesService_ListQrcodeTemplates | QrcodeTemplatesService_List |
| QrcodeTemplatesService_PublicGetQrcodeTemplate | QrcodeTemplatesService_GetPublic |
| QrcodeTemplatesService_PublicListQrcodeTemplates | QrcodeTemplatesService_ListPublic |
| QrcodeTemplatesService_PublishQrcodeTemplate | QrcodeTemplatesService_Publish |
| QrcodeTemplatesService_UpdateQrcodeTemplate | QrcodeTemplatesService_Update |
| SettingsService_GetDataCollection | LinkSettingsService_GetDataCollection |
| SettingsService_GetLinkSetting | LinkSettingsService_Get |
| SettingsService_UpdateDataCollection | LinkSettingsService_UpdateDataCollection |
| SettingsService_UpdateLinkSetting | LinkSettingsService_Update |
| TagsService_Delete | TagsService_BulkDelete |
| WorkflowStepsService_BulkInsertWorkflowStep | WorkflowStepsService_BulkInsert |
| WorkflowStepsService_ConnectStep | WorkflowStepsService_Connect |
| WorkflowStepsService_DisconnectStep | WorkflowStepsService_Disconnect |
| WorkflowStepsService_ResolveStepCollisions | WorkflowStepsService_ResolveCollisions |
| WorkspacesService_GetMyWorkspace | WorkspacesService_Get |
| WorkspacesService_PublicGetWorkspace | WorkspacesService_GetPublic |

Request and response models renamed with them: `PublicCreateQrcodeDesignRequest`
and `...Response` are `CreateQrcodeDesignRequest` and `...Response`,
`CheckCustomDomainResponse` is `VerifyCustomDomainResponse`,
`ShortlinkRandomResponse` is `GenerateShortlinkResponse` and
`ShortlinkAvailabilityResponse` is `CheckShortlinkAvailabilityResponse`.

Four paths changed. The API keeps answering the former ones until at least
2027-06-01 (with `Deprecation` and `Sunset` response headers), so an older
release of this SDK keeps working until then; this release calls the new ones:

| Former path | Current path |
|---|---|
| `POST /v1/visitor/identify` | `POST /v1/visitors:identify` |
| `POST /v1/public/qrcode-designs` | `POST /v1/qrcode-designs` |
| `GET /v1/allowances` | `GET /v1/plan-usage` |
| `POST /v1/custom-domains/{id}/check` | `POST /v1/custom-domains/{id}:verify` |
| `POST /v1/auth/email/verification/request` | `POST /v1/members/email-verification` |

### Moved operation (2026-11-16)

Resending a member's verification email is now in the Members section, so
`authServiceRequestEmailVerification` moves from AuthApi to MembersApi (the
method keeps its name; the operation id is still
`AuthService_RequestEmailVerification`). AuthApi had no other public
operation and goes away. Its path is now `POST /v1/members/email-verification`;
the former `POST /v1/auth/email/verification/request` keeps answering until
at least 2027-06-01. Call it when a call answers `WORKSPACE_UNVERIFIED`: it
sends the verification email again, and verifying the address lifts the pause.

### Other

- POST /v1/links/batch has its own summary, distinct from /v1/links/bulk.
- ErrorResponse.code is documented as the gRPC status code (16 for missing
  credentials), which is what the API has always returned.
