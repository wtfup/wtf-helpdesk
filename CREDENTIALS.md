# WTF Helpdesk Credentials

> **IMPORTANT**: This file contains sensitive credentials. Keep it secure and do not share publicly.

## Production Environment (Azure VM)

### Azure Resources
| Resource | Value |
|----------|-------|
| Resource Group | `wtf-helpdesk-rg` |
| VM Name | `wtf-helpdesk-vm` |
| Location | Central India |
| Public IP | `4.213.96.238` |
| SSH User | `azureuser` |

### Application Credentials
| Service | Username | Password |
|---------|----------|----------|
| Helpdesk Admin | `Administrator` | `WtfAdm1n2026` |
| MariaDB Root | `root` | `WtfH3lpd3sk2026Pr0d` |

### URLs
| Environment | URL |
|-------------|-----|
| Production | https://support.wtfgyms.com |
| Direct IP (temporary) | http://4.213.96.238 |

### SSH Access
```bash
ssh azureuser@4.213.96.238
```

### Docker Commands (on VM)
```bash
# View logs
cd ~/wtf-helpdesk/docker
docker compose -f docker-compose.prod.yml logs -f

# Restart services
docker compose -f docker-compose.prod.yml restart

# Stop all services
docker compose -f docker-compose.prod.yml down

# Start all services
docker compose -f docker-compose.prod.yml up -d
```

## DNS Configuration (AWS Route 53)

Add the following A record:
- **Name**: `support.wtfgyms.com`
- **Type**: A
- **Value**: `4.213.96.238`
- **TTL**: 300

## GitHub Repository

| Item | Value |
|------|-------|
| Repository | https://github.com/wtfup/wtf-helpdesk |
| Visibility | Public |
| Default Branch | `develop` |

---

*Generated on: 2026-01-20*
*Last updated by: Claude Code deployment automation*
