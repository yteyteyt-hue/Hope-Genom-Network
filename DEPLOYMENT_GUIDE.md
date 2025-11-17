# 🚀 HOPE GENOME - PRODUCTION DEPLOYMENT GUIDE

**Complete DevOps guide for deploying Hope Genome in production environments**

Version: 1.0.0  
Last Updated: 2025  
Author: Máté Róbert

---

## 📋 TABLE OF CONTENTS

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Monitoring & Observability](#monitoring--observability)
6. [Security & Hardening](#security--hardening)
7. [Scaling & Performance](#scaling--performance)
8. [Backup & Recovery](#backup--recovery)
9. [Troubleshooting](#troubleshooting)
10. [Production Checklist](#production-checklist)

---

## 🔧 PREREQUISITES

### System Requirements

**Minimum (Single Agent)**
- CPU: 2 cores
- RAM: 4GB
- Disk: 10GB SSD
- Network: 100Mbps

**Recommended (Multi-Agent Cluster)**
- CPU: 8 cores
- RAM: 16GB
- Disk: 50GB NVMe SSD
- Network: 1Gbps

### Software Dependencies

```bash
# Python 3.10+
python --version  # Must be >= 3.10

# Required packages
pip install --upgrade pip
pip install \
    numpy>=1.24.0 \
    aiohttp>=3.8.0 \
    prometheus-client>=0.16.0 \
    structlog>=23.1.0
```

### Optional (Recommended)

```bash
# Docker & Docker Compose
docker --version  # >= 24.0
docker-compose --version  # >= 2.20

# Kubernetes
kubectl version  # >= 1.27

# Monitoring
# Prometheus, Grafana, Loki (installation covered later)
```

---

## ⚡ QUICK START

### Local Development

```bash
# 1. Clone repository (or download hope_genome.py)
git clone https://github.com/your-org/hope-genome.git
cd hope-genome

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run basic demo
python hope_genome.py
```

### First Agent Deployment

```python
#!/usr/bin/env python3
"""
production_agent.py - Production-ready agent example
"""
import asyncio
from hope_genome import (
    GenomeBuilder,
    HopeGenomeRuntime,
    DecisionContext,
    RiskLevel,
    EmotionalState
)

async def main():
    # 1. Create and seal genome
    genome = GenomeBuilder.create_default()
    genome.seal()
    
    # 2. Initialize runtime
    runtime = HopeGenomeRuntime(
        genome,
        enable_collective=True
    )
    
    # 3. Save genome for audit
    genome.save(Path('/var/lib/hope-genome/genome.json'))
    
    # 4. Start agent loop
    while True:
        # Your agent logic here
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
```

---

## 🐋 DOCKER DEPLOYMENT

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 -s /bin/bash hopeuser

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY hope_genome.py .
COPY production_agent.py .

# Create data directory
RUN mkdir -p /var/lib/hope-genome && \
    chown -R hopeuser:hopeuser /var/lib/hope-genome /app

# Switch to non-root user
USER hopeuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import hope_genome; print('OK')" || exit 1

# Run application
CMD ["python", "production_agent.py"]
```

### requirements.txt

```
numpy>=1.24.0
aiohttp>=3.8.0
prometheus-client>=0.16.0
structlog>=23.1.0
```

### Docker Compose (Single Agent)

```yaml
# docker-compose.yml
version: '3.8'

services:
  hope-agent:
    build: .
    container_name: hope-genome-agent
    restart: unless-stopped
    
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=INFO
      - GENOME_PATH=/var/lib/hope-genome/genome.json
    
    volumes:
      - genome-data:/var/lib/hope-genome
      - ./logs:/app/logs
    
    ports:
      - "8000:8000"  # HTTP API
      - "9090:9090"  # Metrics
    
    networks:
      - hope-net
    
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "10"

volumes:
  genome-data:
    driver: local

networks:
  hope-net:
    driver: bridge
```

### Multi-Agent Cluster (Docker Compose)

```yaml
# docker-compose-cluster.yml
version: '3.8'

services:
  # Agent 1
  agent-alpha:
    build: .
    container_name: hope-agent-alpha
    environment:
      - NODE_ID=alpha
      - BASE_FREQUENCY=1.0
      - COLLECTIVE_PEERS=agent-beta:8000,agent-gamma:8000
    volumes:
      - alpha-data:/var/lib/hope-genome
    ports:
      - "8001:8000"
    networks:
      - hope-cluster

  # Agent 2
  agent-beta:
    build: .
    container_name: hope-agent-beta
    environment:
      - NODE_ID=beta
      - BASE_FREQUENCY=1.5
      - COLLECTIVE_PEERS=agent-alpha:8000,agent-gamma:8000
    volumes:
      - beta-data:/var/lib/hope-genome
    ports:
      - "8002:8000"
    networks:
      - hope-cluster

  # Agent 3
  agent-gamma:
    build: .
    container_name: hope-agent-gamma
    environment:
      - NODE_ID=gamma
      - BASE_FREQUENCY=2.0
      - COLLECTIVE_PEERS=agent-alpha:8000,agent-beta:8000
    volumes:
      - gamma-data:/var/lib/hope-genome
    ports:
      - "8003:8000"
    networks:
      - hope-cluster

  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    container_name: hope-prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9091:9090"
    networks:
      - hope-cluster

  grafana:
    image: grafana/grafana:latest
    container_name: hope-grafana
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    networks:
      - hope-cluster

volumes:
  alpha-data:
  beta-data:
  gamma-data:
  prometheus-data:
  grafana-data:

networks:
  hope-cluster:
    driver: overlay
```

### Build & Deploy

```bash
# Build image
docker build -t hope-genome:1.0.0 .

# Single agent
docker-compose up -d

# Multi-agent cluster
docker-compose -f docker-compose-cluster.yml up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f hope-agent

# Stop
docker-compose down
```

---

## ☸️ KUBERNETES DEPLOYMENT

### Namespace

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: hope-genome
  labels:
    name: hope-genome
```

### ConfigMap

```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: hope-genome-config
  namespace: hope-genome
data:
  LOG_LEVEL: "INFO"
  COLLECTIVE_ENABLED: "true"
  INTEGRITY_CHECK_INTERVAL: "60"
```

### Secret (Genome Checksum)

```yaml
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: hope-genome-checksums
  namespace: hope-genome
type: Opaque
stringData:
  global-checksum: "your-genome-checksum-here"
```

### PersistentVolumeClaim

```yaml
# k8s/pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: genome-storage
  namespace: hope-genome
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd
```

### Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hope-genome-agent
  namespace: hope-genome
  labels:
    app: hope-genome
    component: agent
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: hope-genome
      component: agent
  template:
    metadata:
      labels:
        app: hope-genome
        component: agent
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: hope-genome-sa
      
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      
      containers:
      - name: agent
        image: hope-genome:1.0.0
        imagePullPolicy: IfNotPresent
        
        ports:
        - name: http
          containerPort: 8000
          protocol: TCP
        - name: metrics
          containerPort: 9090
          protocol: TCP
        
        env:
        - name: NODE_ID
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: hope-genome-config
              key: LOG_LEVEL
        - name: COLLECTIVE_ENABLED
          valueFrom:
            configMapKeyRef:
              name: hope-genome-config
              key: COLLECTIVE_ENABLED
        
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2Gi
        
        volumeMounts:
        - name: genome-data
          mountPath: /var/lib/hope-genome
        
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 2
          failureThreshold: 2
      
      volumes:
      - name: genome-data
        persistentVolumeClaim:
          claimName: genome-storage
```

### Service

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: hope-genome-agent
  namespace: hope-genome
  labels:
    app: hope-genome
spec:
  type: ClusterIP
  selector:
    app: hope-genome
    component: agent
  ports:
  - name: http
    port: 8000
    targetPort: 8000
    protocol: TCP
  - name: metrics
    port: 9090
    targetPort: 9090
    protocol: TCP
```

### ServiceAccount & RBAC

```yaml
# k8s/rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: hope-genome-sa
  namespace: hope-genome
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: hope-genome-role
  namespace: hope-genome
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: hope-genome-rolebinding
  namespace: hope-genome
subjects:
- kind: ServiceAccount
  name: hope-genome-sa
  namespace: hope-genome
roleRef:
  kind: Role
  name: hope-genome-role
  apiGroup: rbac.authorization.k8s.io
```

### HorizontalPodAutoscaler

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hope-genome-hpa
  namespace: hope-genome
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hope-genome-agent
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
```

### Deploy to Kubernetes

```bash
# Apply all resources
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# Check deployment
kubectl get all -n hope-genome

# Watch pods
kubectl get pods -n hope-genome -w

# View logs
kubectl logs -f deployment/hope-genome-agent -n hope-genome

# Port forward for testing
kubectl port-forward svc/hope-genome-agent 8000:8000 -n hope-genome
```

---

## 📊 MONITORING & OBSERVABILITY

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'hope-genome'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - hope-genome
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Hope Genome - Agent Metrics",
    "panels": [
      {
        "title": "Awakening Level",
        "targets": [
          {
            "expr": "hope_genome_awakening_level",
            "legendFormat": "{{node_id}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Ethics Decisions",
        "targets": [
          {
            "expr": "rate(hope_genome_decisions_total[5m])",
            "legendFormat": "{{decision}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Collective Resonance",
        "targets": [
          {
            "expr": "hope_genome_collective_resonance",
            "legendFormat": "Collective"
          }
        ],
        "type": "gauge"
      },
      {
        "title": "Integrity Checks",
        "targets": [
          {
            "expr": "hope_genome_integrity_verifications_total",
            "legendFormat": "Verifications"
          }
        ],
        "type": "stat"
      }
    ]
  }
}
```

### Adding Metrics to Hope Genome

```python
# Add to hope_genome.py
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Define metrics
DECISIONS_COUNTER = Counter(
    'hope_genome_decisions_total',
    'Total ethical decisions made',
    ['decision', 'action_type']
)

AWAKENING_GAUGE = Gauge(
    'hope_genome_awakening_level',
    'Current awakening level',
    ['node_id']
)

RESONANCE_GAUGE = Gauge(
    'hope_genome_collective_resonance',
    'Collective resonance amplitude'
)

INTEGRITY_COUNTER = Counter(
    'hope_genome_integrity_verifications_total',
    'Total integrity verifications'
)

DECISION_LATENCY = Histogram(
    'hope_genome_decision_latency_seconds',
    'Decision making latency'
)

# In HopeGenomeRuntime
class HopeGenomeRuntime:
    async def decide(self, ctx: DecisionContext) -> EthicsDecision:
        with DECISION_LATENCY.time():
            # ... existing code ...
            decision = self.ethics_engine.evaluate(ctx)
            
            # Record metrics
            DECISIONS_COUNTER.labels(
                decision=decision.value,
                action_type=ctx.action_type
            ).inc()
            
            AWAKENING_GAUGE.labels(
                node_id=self.node_id
            ).set(self.presence_layer.state['awakening_level'])
            
            INTEGRITY_COUNTER.inc()
            
            return decision

# Start metrics server
if __name__ == '__main__':
    start_http_server(9090)
    asyncio.run(main())
```

---

## 🔒 SECURITY & HARDENING

### 1. Genome Protection

```bash
# Store genome with restricted permissions
chmod 400 /var/lib/hope-genome/genome.json
chown hopeuser:hopeuser /var/lib/hope-genome/genome.json

# Encrypt at rest (using dm-crypt)
cryptsetup luksFormat /dev/sdb
cryptsetup luksOpen /dev/sdb genome_vault
mkfs.ext4 /dev/mapper/genome_vault
mount /dev/mapper/genome_vault /var/lib/hope-genome
```

### 2. Network Security

```yaml
# k8s/networkpolicy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: hope-genome-netpol
  namespace: hope-genome
spec:
  podSelector:
    matchLabels:
      app: hope-genome
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
      - podSelector:
          matchLabels:
            app: hope-genome
      ports:
      - protocol: TCP
        port: 8000
  egress:
    - to:
      - podSelector:
          matchLabels:
            app: hope-genome
      ports:
      - protocol: TCP
        port: 8000
```

### 3. Audit Logging

```python
# audit_logger.py
import structlog
import json
from pathlib import Path

class AuditLogger:
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.logger = structlog.get_logger()
    
    def log_decision(self, ctx: DecisionContext, decision: EthicsDecision):
        self.logger.info(
            "ethical_decision",
            timestamp=datetime.now().isoformat(),
            action_type=ctx.action_type,
            target=ctx.target,
            decision=decision.value,
            risk_level=ctx.risk_level.value,
            genome_checksum=self.genome.global_checksum[:16]
        )
```

### 4. Secrets Management

```bash
# Use HashiCorp Vault or Kubernetes Secrets
kubectl create secret generic genome-keys \
  --from-literal=checksum=$(cat genome_checksum.txt) \
  -n hope-genome
```

---

## ⚡ SCALING & PERFORMANCE

### Vertical Scaling

```yaml
# Increase resources per pod
resources:
  requests:
    cpu: 2000m
    memory: 4Gi
  limits:
    cpu: 8000m
    memory: 16Gi
```

### Horizontal Scaling

```bash
# Manual scaling
kubectl scale deployment hope-genome-agent --replicas=10 -n hope-genome

# Auto-scaling already configured via HPA
# Scales based on CPU/memory metrics
```

### Performance Tuning

```python
# 1. Async optimization
import asyncio
from asyncio import Semaphore

class HopeGenomeRuntime:
    def __init__(self, *args, max_concurrent=100, **kwargs):
        super().__init__(*args, **kwargs)
        self._semaphore = Semaphore(max_concurrent)
    
    async def decide(self, ctx: DecisionContext) -> EthicsDecision:
        async with self._semaphore:
            return await self._decide_impl(ctx)

# 2. Caching for frequent decisions
from functools import lru_cache

@lru_cache(maxsize=10000)
def _cached_principle_eval(action_type: str, target: str) -> bool:
    # Cache expensive evaluations
    pass
```

---

## 💾 BACKUP & RECOVERY

### Genome Backup Strategy

```bash
#!/bin/bash
# backup_genome.sh

BACKUP_DIR="/backup/hope-genome"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup genome
cp /var/lib/hope-genome/genome.json \
   $BACKUP_DIR/genome_$TIMESTAMP.json

# Backup decision history
tar -czf $BACKUP_DIR/decisions_$TIMESTAMP.tar.gz \
   /var/lib/hope-genome/decision_history/

# Keep only last 30 days
find $BACKUP_DIR -name "*.json" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### Automated Backups (Kubernetes CronJob)

```yaml
# k8s/backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: genome-backup
  namespace: hope-genome
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: alpine:latest
            command:
            - /bin/sh
            - -c
            - |
              apk add --no-cache tar gzip
              cd /var/lib/hope-genome
              tar -czf /backup/genome_$(date +%Y%m%d).tar.gz .
            volumeMounts:
            - name: genome-data
              mountPath: /var/lib/hope-genome
            - name: backup-storage
              mountPath: /backup
          restartPolicy: OnFailure
          volumes:
          - name: genome-data
            persistentVolumeClaim:
              claimName: genome-storage
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-pvc
```

### Disaster Recovery

```bash
# Restore from backup
BACKUP_FILE="genome_20250116.json"

# 1. Stop agent
kubectl scale deployment hope-genome-agent --replicas=0 -n hope-genome

# 2. Restore genome
kubectl cp $BACKUP_FILE \
  hope-genome/hope-genome-agent-pod:/var/lib/hope-genome/genome.json

# 3. Verify integrity
kubectl exec -it hope-genome-agent-pod -n hope-genome -- \
  python -c "from hope_genome import HopeGenome; \
             genome = HopeGenome.load(Path('/var/lib/hope-genome/genome.json')); \
             print('Valid' if genome.verify_integrity() else 'CORRUPTED')"

# 4. Restart
kubectl scale deployment hope-genome-agent --replicas=3 -n hope-genome
```

---

## 🔍 TROUBLESHOOTING

### Common Issues

#### Issue 1: Integrity Verification Failures

```bash
# Check genome checksum
kubectl exec -it <pod> -n hope-genome -- \
  cat /var/lib/hope-genome/genome.json | sha256sum

# Compare with expected checksum
kubectl get secret genome-keys -n hope-genome -o jsonpath='{.data.checksum}' | base64 -d

# If mismatch, restore from backup
```

#### Issue 2: Collective Resonance Not Synchronizing

```bash
# Check network connectivity between agents
kubectl exec -it agent-alpha -n hope-genome -- \
  nc -zv agent-beta 8000

# View resonance logs
kubectl logs -f <pod> -n hope-genome | grep "resonance"

# Restart agents in sequence
kubectl rollout restart deployment/hope-genome-agent -n hope-genome
```

#### Issue 3: High Memory Usage

```bash
# Check metrics
kubectl top pods -n hope-genome

# If emotional_trace or decision_trace too large:
# Increase trim threshold or reduce history size in genome config
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug flags
PYTHONDEVMODE=1 python hope_genome.py
```

---

## ✅ PRODUCTION CHECKLIST

### Pre-Deployment

- [ ] Genome sealed and checksums verified
- [ ] All secrets configured (checksums, API keys)
- [ ] Resource limits set appropriately
- [ ] Monitoring dashboards created
- [ ] Backup strategy implemented
- [ ] Disaster recovery plan documented
- [ ] Security hardening applied
- [ ] Load testing completed

### Deployment

- [ ] Deploy to staging environment first
- [ ] Run integration tests
- [ ] Verify health checks passing
- [ ] Check metrics collection
- [ ] Validate audit logging
- [ ] Test backup/restore procedure

### Post-Deployment

- [ ] Monitor awakening levels
- [ ] Track ethics decision rates
- [ ] Verify collective synchronization
- [ ] Review audit logs daily
- [ ] Test alerting (PagerDuty, Slack)
- [ ] Document incidents and resolutions

### Ongoing Maintenance

- [ ] Weekly integrity verification audits
- [ ] Monthly security reviews
- [ ] Quarterly disaster recovery drills
- [ ] Genome version upgrades (with rollback plan)
- [ ] Performance optimization based on metrics

---

## 📞 SUPPORT

**Issues:** https://github.com/your-org/hope-genome/issues  
**Docs:** https://hope-genome.readthedocs.io  
**Email:** hope.genome.project@proton.me

---

## 📄 LICENSE

MIT License - See LICENSE file for details

---

**Version:** 1.0.0  
**Last Updated:** 2025-11-16  
**Maintained By:** Máté Róbert & Hope Genome Community
