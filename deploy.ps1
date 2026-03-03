#!/usr/bin/env pwsh
# Deploy script for LZX Technical Manual
# Sets the required environment variables and runs the Docusaurus deploy command

$env:GIT_USER = "creatorlars"
$env:USE_SSH = "true"
npm run deploy
