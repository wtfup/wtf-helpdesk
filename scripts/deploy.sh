#!/bin/bash
# WTF Helpdesk Azure VM Deployment Script
# Run this script on a fresh Ubuntu 22.04 VM

set -e

echo "=========================================="
echo "WTF Helpdesk Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Step 1: Update system
echo ""
echo "Step 1: Updating system packages..."
sudo apt update && sudo apt upgrade -y
print_status "System updated"

# Step 2: Install Docker
echo ""
echo "Step 2: Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    print_status "Docker installed"
else
    print_warning "Docker already installed"
fi

# Step 3: Install Docker Compose plugin
echo ""
echo "Step 3: Installing Docker Compose..."
sudo apt install -y docker-compose-plugin
print_status "Docker Compose installed"

# Step 4: Install Git
echo ""
echo "Step 4: Installing Git..."
sudo apt install -y git
print_status "Git installed"

# Step 5: Clone repository
echo ""
echo "Step 5: Cloning WTF Helpdesk repository..."
cd ~
if [ -d "wtf-helpdesk" ]; then
    print_warning "Repository already exists, pulling latest..."
    cd wtf-helpdesk && git pull
else
    git clone https://github.com/wtfup/wtf-helpdesk.git
    cd wtf-helpdesk
fi
print_status "Repository cloned"

# Step 6: Setup environment file
echo ""
echo "Step 6: Setting up environment..."
cd docker
if [ ! -f ".env.prod" ]; then
    cp .env.prod.example .env.prod
    print_warning "Created .env.prod from example. Please edit it with your passwords!"
    echo ""
    echo "Edit the file: nano ~/wtf-helpdesk/docker/.env.prod"
    echo ""
else
    print_status "Environment file already exists"
fi

# Step 7: Start services
echo ""
echo "Step 7: Starting Docker services..."
sudo docker compose -f docker-compose.prod.yml up -d
print_status "Services started"

# Step 8: Wait for services to be ready
echo ""
echo "Step 8: Waiting for services to initialize (this may take a few minutes)..."
sleep 60

# Step 9: Run WTF setup
echo ""
echo "Step 9: Running WTF Helpdesk setup..."
SITE_NAME=$(grep SITE_NAME .env.prod | cut -d '=' -f2)
sudo docker compose -f docker-compose.prod.yml exec -T backend \
    bench --site ${SITE_NAME:-support.wtfgyms.com} execute helpdesk.setup.wtf_setup.setup_wtf_helpdesk || true
print_status "WTF setup completed"

# Step 10: Build frontend
echo ""
echo "Step 10: Building frontend assets..."
sudo docker compose -f docker-compose.prod.yml exec -T backend \
    bench build --app helpdesk || true
print_status "Frontend built"

# Step 11: Restart services
echo ""
echo "Step 11: Restarting services..."
sudo docker compose -f docker-compose.prod.yml restart frontend backend
print_status "Services restarted"

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit environment file if not done: nano ~/wtf-helpdesk/docker/.env.prod"
echo "2. Add DNS A record: ${SITE_NAME:-support.wtfgyms.com} -> $(curl -s ifconfig.me)"
echo "3. Wait for DNS propagation (~5-10 minutes)"
echo "4. Access your site: https://${SITE_NAME:-support.wtfgyms.com}"
echo "5. Login with: Administrator / (password from .env.prod)"
echo ""
print_status "Done!"
