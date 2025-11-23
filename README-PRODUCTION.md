# Production Monitoring Environment

## Overview

This is a comprehensive production monitoring setup with Prometheus, Grafana, Loki, Alertmanager, and multiple exporters for full observability.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Application   │    │   PostgreSQL    │    │     Redis       │
│   (FastAPI)     │    │   (Database)    │    │    (Cache)      │
│   Port: 8003    │    │   Port: 5432    │    │   Port: 6379    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Prometheus    │    │    Grafana      │    │     Loki        │
│   (Metrics)     │    │  (Dashboards)   │    │    (Logs)       │
│   Port: 9090    │    │   Port: 3040    │    │   Port: 3100    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Alertmanager   │    │   Exporters     │    │    Promtail     │
│   (Alerts)      │    │  (All Services) │    │   (Log Shipper) │
│   Port: 9093    │    │  (See Below)    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Services and Ports

### Core Services
- **Application**: http://localhost:8003
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3040 (admin/admin)
- **Loki**: http://localhost:3100
- **Alertmanager**: http://localhost:9093

### Exporters
- **PostgreSQL Exporter**: http://localhost:9187/metrics
- **Redis Exporter**: http://localhost:9121/metrics
- **Node Exporter**: http://localhost:9100/metrics
- **Nginx Exporter**: http://localhost:9113/metrics
- **cAdvisor**: http://localhost:8080/metrics

## Quick Start

1. **Configure Environment**:
   ```bash
   cp .env.prod.example .env.prod
   # Edit .env.prod with your actual values
   ```

2. **Start All Services**:
   ```bash
   ./scripts/start-prod.sh
   ```

3. **Verify Setup**:
   ```bash
   docker-compose -f docker-compose-prod.yml ps
   ```

## Configuration

### Prometheus Configuration
- **Main config**: `prometheus.yml`
- **Alert rules**: `alerts/production_alerts.yml`
- **Recording rules**: `recording_rules/production_rules.yml`
- **Storage**: 30 days retention
- **Scrape interval**: 15s

### Alertmanager Configuration
- **Config**: `alertmanager.yml`
- **Receivers**: Slack, Email
- **Routing**: By severity and service

### Grafana Configuration
- **Datasources**: Prometheus, Loki
- **Dashboards**: Auto-provisioned
- **Authentication**: Admin/admin (change immediately)

## Monitoring Features

### Application Metrics
- Request rate and latency
- Error rate and status codes
- Active connections
- Custom business metrics

### Database Metrics
- Connection pool usage
- Query performance
- Lock statistics
- Replication lag

### System Metrics
- CPU, memory, disk usage
- Network traffic
- Process statistics
- Load average

### Container Metrics
- Container resource usage
- Image statistics
- Volume usage
- Network statistics

### Log Aggregation
- Application logs
- System logs
- Docker container logs
- Structured log parsing

## Alerting

### Critical Alerts
- Service down
- High error rate
- Database unavailable
- High memory usage
- Disk space low

### Warning Alerts
- High latency
- Slow queries
- High CPU usage
- Memory pressure
- Network issues

## Security Considerations

1. **Change default passwords**:
   - Grafana admin password
   - Database passwords
   - Application secrets

2. **Configure SSL/TLS**:
   - Place certificates in `nginx/ssl/`
   - Update nginx configuration

3. **Network Security**:
   - Use internal Docker networks
   - Restrict external access to monitoring endpoints

4. **Sensitive Data**:
   - Never commit `.env.prod`
   - Use secrets management for production

## Maintenance

### Backup
```bash
# Backup Prometheus data
docker run --rm -v test_c_sharp_prometheus_data:/data -v $(pwd):/backup alpine tar czf /backup/prometheus-backup.tar.gz /data

# Backup Grafana data
docker run --rm -v test_c_sharp_grafana_data:/data -v $(pwd):/backup alpine tar czf /backup/grafana-backup.tar.gz /data
```

### Updates
```bash
# Update all images
docker-compose -f docker-compose-prod.yml pull
docker-compose -f docker-compose-prod.yml up -d

# Check for updates
docker-compose -f docker-compose-prod.yml images | grep -v REPOSITORY | awk '{print $1":"$2}' | xargs -I {} docker pull {}
```

### Log Management
```bash
# View service logs
docker-compose -f docker-compose-prod.yml logs -f [service_name]

# Clean up old logs
docker system prune -f
```

## Troubleshooting

### Common Issues

1. **Service won't start**:
   ```bash
   docker-compose -f docker-compose-prod.yml logs [service_name]
   ```

2. **Prometheus targets down**:
   - Check http://localhost:9090/targets
   - Verify exporter endpoints
   - Check network connectivity

3. **No data in Grafana**:
   - Verify datasource configuration
   - Check Prometheus targets
   - Import dashboards

4. **Alerts not firing**:
   - Check Alertmanager configuration
   - Verify alert rules in Prometheus
   - Test notification channels

### Health Checks

All services include health check endpoints:
- Prometheus: http://localhost:9090/-/healthy
- Grafana: http://localhost:3040/api/health
- Loki: http://localhost:3100/ready
- Alertmanager: http://localhost:9093/-/healthy

## Performance Tuning

### Prometheus
- Adjust retention period based on storage
- Configure recording rules for complex queries
- Use remote storage for long-term retention

### Grafana
- Enable query caching
- Optimize dashboard queries
- Use template variables efficiently

### Application
- Configure appropriate log levels
- Use structured logging
- Implement proper error handling

## Support

For issues and questions:
1. Check service logs
2. Verify configuration files
3. Test endpoints manually
4. Review monitoring best practices