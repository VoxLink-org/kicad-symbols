# KiCad Symbols Mirror

This repository is a mirror of the official KiCad symbols library from GitLab, automatically synced daily.

## Source Repository
- **Original**: https://gitlab.com/kicad/libraries/kicad-symbols.git
- **Mirror**: This repository

## Automatic Sync

This repository uses GitHub Actions to automatically sync from the upstream GitLab repository daily at 2 AM UTC. The sync includes:

- Master branch only
- Complete repository history

### Manual Sync

You can also manually trigger a sync by:
1. Going to the [Actions tab](../../actions) in this repository
2. Selecting "Sync from GitLab" workflow
3. Clicking "Run workflow"

### Setup Requirements

The sync action runs automatically without any additional setup. However, ensure that:

1. The repository has GitHub Actions enabled
2. The default branch permissions allow force pushes (required for sync)

### Sync Behavior

- **Force Push**: The sync uses force push to ensure complete alignment with the upstream repository
- **Overwrite**: Any changes in this mirror will be overwritten by the upstream changes
- **Complete Sync**: All branches, tags, and history are synchronized

## Usage

This mirror can be used as a fallback or alternative source for KiCad symbols, especially in environments where GitLab access might be restricted.

## Contributing

Since this is a mirror repository, all contributions should be made to the original GitLab repository at https://gitlab.com/kicad/libraries/kicad-symbols.git