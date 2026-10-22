# Security

Please report a vulnerability privately to **contact@lacobble.dev** (or through https://support.lacobble.dev),
not in a public issue. You will get an answer within a few days.

Only the current `main` branch is maintained.

The daily workflow uses a personal token (`GH_PAT`, repository secret) that only reads repository language totals;
the generated files never contain the name of a private repository. A leaked token must be revoked at
https://github.com/settings/tokens first, then replaced in the repository secrets.
