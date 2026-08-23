# Surface Checklists — MMP Health & Cross-Device Attribution

Read when the audited account runs mobile app campaigns or needs
cross-device stitching. Reference for `smartpowers:ads-attribution`.

## MMP Health (Mobile Apps)

- **MMP integrated** — AppsFlyer / Adjust / Branch / Singular set up before
  any paid campaigns launched
- **Apple Ads connected as a partner** in MMP dashboard
- **Post-install events sent back** to Apple Ads, Google UAC, Meta App
  Campaigns, TikTok (enables Maximize Conversions and ROAS bidding)
- **Event quality**: purchase, subscription_start, trial_start, or other
  revenue events tracked (not just install → registration)
- **Postback configuration**: SKAN/AAK conversion values map to meaningful
  user actions

## Cross-Device & Cross-Platform Attribution

- **Customer Match** lists synced to Google Ads, Meta (Customer File CA),
  LinkedIn Matched Audiences, TikTok Customer File for cross-device stitching
- **Enhanced Conversions** active for Google Ads (hashed first-party data,
  ~10% uplift on properly-implemented setups)
- **CAPI customer_information parameters** (`em`, `ph`, `fn`, `ln`, `ct`,
  `st`, `zp`, `external_id`) sent server-side to Meta
- **Privacy-safe identifiers** (Customer Match hashes, GAID/IDFA where
  permitted) included in conversion exports
