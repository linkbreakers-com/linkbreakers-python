# Changelog

## Next release after 1.200.0 (2026-11-16): files are uploaded, never sent in a request

Breaking for code sending a file in a request. Versions follow the API's
version.

A file reaches Linkbreakers one way: uploaded straight to storage, which gives
a media id, and every field that takes a file takes that id. Removed, with no
outside caller in the last 14 days:

| Removed | Use instead |
|---|---|
| `MediaApi.media_service_create` (and `CreateMediaRequest`, `CreateMediaResponse`) (`POST /v1/media`, the file base64 in the request) | `media_service_create_upload`, a PUT to `upload_url`, then `media_service_complete_upload` |
| `central_image_data` on QR code design create and update (the logo base64) | `central_image_media_id`: an image of your media library on update; a public upload on create |

Added: `media_service_create_public_upload` and `media_service_complete_public_upload` (`POST /v1/media/public-uploads`, no token), the logo upload for
a QR code design created without a token.

## Next release after 1.200.0 (2026-11-16): four operations join the section they belong to

Breaking for code calling the four operations below. Versions follow the
API's version.

The API moved four operations into the section, and the service, they are
about. Each section is one API class, and the method name comes from the
operation ID, so the class changes for all four and the method name for
three:

| Before | After |
|---|---|
| `APIScopesApi.workspace_tokens_service_list_api_scopes` | `WorkspaceTokensApi.workspace_tokens_service_list_api_scopes` |
| `IntegrationsApi.integrations_service_list_for_link` | `LinksApi.links_service_list_integrations` |
| `MembersApi.auth_service_request_email_verification` | `MembersApi.members_service_request_email_verification` |
| `PlanUsageApi.plan_usage_service_list` | `WorkspacesApi.workspaces_service_get_usage` |

| Operation | Path |
|---|---|
| List the scopes a token can have | `GET /v1/workspace-tokens/scopes` (was `GET /v1/api-scopes`, removed with no alias: no integration called it in the last 14 days) |
| List the integrations active on a link | `GET /v1/links/{linkId}/integrations` (unchanged) |
| Resend a member's verification email | `POST /v1/members/email-verification` (unchanged) |
| Get the workspace's plan usage | `GET /v1/workspace/usage` (was `GET /v1/plan-usage`, removed with no alias: only our dashboard called it) |

The API Scopes, Integrations and Plan Usage classes are gone (the `Integrations*` classes
for Slack, forms, contact tools, Google Analytics and retargeting pixels stay).
`ListAllowancesResponse` is now `WorkspaceUsage`; other models keep their names (`ListApiScopesResponse`, `LinkIntegration`,
`ListLinkIntegrationsResponse`, `RequestEmailVerificationRequest`).

## 1.198.1 to 1.200.0 (2026-11-15 and 2026-11-16): the public API contract cleanup

Breaking for code written against 1.198.0 or earlier. Versions follow the
API's version. The renamed and removed classes, operations and paths below
shipped in 1.198.1; the verification email moved to Members in 1.199.0; the
former paths were removed and Google Forms became one of the form tools in
1.200.0.

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
| GoogleFormsIntegrationsApi | removed: Google Forms is a form tool, see below |
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

Paths changed too, and this release calls the new ones. The API removes a
former path once no client has called it for 14 days; the production logs
showed no outside call on any of them, so they are all gone and an older
release of this SDK gets `404` there:

| Former path | Current path |
|---|---|
| `POST /v1/visitor/identify` | `POST /v1/visitors:identify` |
| `POST /v1/public/qrcode-designs` | `POST /v1/qrcode-designs` |
| `GET /v1/allowances` | `GET /v1/plan-usage` |
| `POST /v1/allowances/dismiss` | `POST /v1/plan-usage/dismiss` |
| `POST /v1/custom-domains/{id}/check` | `POST /v1/custom-domains/{id}:verify` |
| `POST /v1/auth/email/verification/request` | `POST /v1/members/email-verification` |

### Moved operation (2026-11-16)

Resending a member's verification email is now in the Members section, so
`authServiceRequestEmailVerification` moves from AuthApi to MembersApi (the
method keeps its name; the operation id is still
`AuthService_RequestEmailVerification`). AuthApi had no other public
operation and goes away. Its path is now `POST /v1/members/email-verification`;
the former `POST /v1/auth/email/verification/request` is removed (only the
dashboard called it). Call it when a call answers `WORKSPACE_UNVERIFIED`: it
sends the verification email again, and verifying the address lifts the pause.

### Other

- POST /v1/links/batch has its own summary, distinct from /v1/links/bulk.
- ErrorResponse.code is documented as the gRPC status code (16 for missing
  credentials), which is what the API has always returned.

### Google Forms is one of the form tools (2026-11-16)

Google Forms and the other form tools were two separate parts of the API. Google
Forms is now the tool `FORM_TOOL_GOOGLE_FORMS` of IntegrationsFormsApi, under
`/v1/form-integrations/{tool}`, and the Integrations: Google Forms section is
gone, so IntegrationsGoogleFormsApi (GoogleFormsIntegrationsApi before) and its
models (`GoogleFormsIntegration`, `GoogleFormsIntegrationStatus`,
`DetectedGoogleForm`, ...) go away. Over the 14 days before the change nothing
outside the Linkbreakers dashboard called `/v1/google-forms-integrations`; it is
removed with no alias, and an older release gets `404` there.

| Before (GoogleFormsIntegrationsService_...) | After (FormIntegrationsService_..., tool `FORM_TOOL_GOOGLE_FORMS`) |
|---|---|
| Get | Get |
| Update | Update (status `ACTIVE` or `PAUSED`, delivery) |
| Delete | Disconnect |
| ListDetectedForms | ListForms |
| SyncNow | PrepareForms (reads the new responses now, then lists the forms) |
| ChooseFormLink | ChooseFormLink (new: `POST /v1/form-integrations/{tool}/forms/{formId}/link`) |

New in the form tools models: `FormTool.FORM_TOOL_GOOGLE_FORMS`,
`FormConnectionStatus.FORM_CONNECTION_STATUS_ACCESS_REVOKED` (Google access
removed: disconnect and connect again), `FormConnection.lastSyncedAt`,
`FormReadiness.FORM_READINESS_NEEDS_ACCESS` and
`FORM_READINESS_OTHER_LINK_CHOSEN`, `DetectedToolForm.shared` and `chosen`, and
the `ChooseFormToolFormLinkRequest` body. `Connect` with an API key answers
`FORM_TOOL_SIGN_IN_REQUIRED` for Google Forms, which connects by signing in to
Google in the dashboard.
