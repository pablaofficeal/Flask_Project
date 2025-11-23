#!/bin/bash

# Production Environment Setup Script

echo "🚀 Setting up Production Monitoring Environment..."

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Load environment variables
if [ -f .env.prod ]; then
    echo "📋 Loading production environment variables..."
    export $(cat .env.prod | grep -v '^#' | xargs)
else
    echo "⚠️  .env.prod file not found. Using default settings."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p alerts recording_rules grafana/provisioning/datasources grafana/provisioning/dashboards nginx/ssl logs

# Set proper permissions
echo "🔒 Setting proper permissions..."
chmod 600 .env.prod 2>/dev/null || true
chmod +x scripts/*.sh 2>/dev/null || true

# Build and start all services
echo "🏗️  Building and starting all services..."
docker-compose -f docker-compose-prod.yml down --remove-orphans
docker-compose -f docker-compose-prod.yml build --no-cache
docker-compose -f docker-compose-prod.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🏥 Checking service health..."
services=("prometheus" "grafana" "loki" "alertmanager" "app" "db" "regis" "nginx")

for service in "${services[@]}"; do
    if docker-compose -f docker-compose-prod.yml ps | grep -q "$service.*Up"; then
        echo "✅ $service is running"
    else
        echo "❌ $service is not running"
    fi
done

# Test endpoints
echo "🧪 Testing endpoints..."
endpoints=(
    "http://localhost:9090/-/healthy:Prometheus"
    "http://localhost:3040/api/health:Grafana"
    "http://localhost:3100/ready:Loki"
    "http://localhost:9093/-/healthy:Alertmanager"
    "http://localhost:8003/test-api:Application"
)

for endpoint_info in "${endpoints[@]}"; do
    IFS=':' read -r endpoint name <<< "$endpoint_info"
    if curl -s -f "$endpoint" > /dev/null; then
        echo "✅ $name endpoint is accessible"
    else
        echo "⚠️  $name endpoint check failed (this might be normal during startup)"
    fi
done

echo ""
echo "🎉 Production monitoring environment is ready!"
echo ""
echo "📊 Access your services:"
echo "  🎯 Application:      http://localhost:8003"
echo "  📈 Prometheus:       http://localhost:9090"
echo "  📊 Grafana:          http://localhost:3040 (admin/admin)"
echo "  📋 Loki:             http://localhost:3100"
echo "  🚨 Alertmanager:   http://localhost:9093"
echo ""
echo "📁 Service endpoints:"
echo "  📊 Prometheus:       http://localhost:9090/metrics"
echo "  🐘 PostgreSQL Exp:   http://localhost:9187/metrics"
echo "  🔴 Redis Exp:        http://localhost:9121/metrics"
echo "  🖥️  Node Exp:         http://localhost:9100/metrics"
echo "  🌐 Nginx Exp:        http://localhost:9113/metrics"
echo "  🐳 cAdvisor:         http://localhost:8080/metrics"
echo ""
echo "⚠️  Don't forget to:"
echo "  1. Update .env.prod with your actual credentials"
echo "  2. Configure Slack webhook URL for alerts"
echo "  3. Set up SSL certificates in nginx/ssl/"
echo "  4. Import Grafana dashboards"
echo "  5. Configure alert rules as needed"
echo ""
echo "To stop all services: docker-compose -f docker-compose-prod.yml down"
echo "To view logs: docker-compose -f docker-compose-prod.yml logs -f [service_name]"