#!/bin/bash

echo " Starting all resource containers..."
docker-compose -f docker-compose.resources.yml up -d

echo "✅ All resources are up."