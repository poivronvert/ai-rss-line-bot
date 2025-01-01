VERSION:=0.0.1
all: buildimg test pushimg-gcp

buildimg:
	podman build -t redis-cloud-run:$(VERSION) .

test: buildimg
	podman rm -f redis-cloud-run-testing-only > /dev/null || true;
	podman run -d --name redis-cloud-run-testing-only -p 6379:6379 redis-cloud-run:$(VERSION); 
	@sleep 10;
	@if podman ps --filter "name=redis-cloud-run-testing-only" --format "{{.Names}}" | grep -q redis-cloud-run-testing-only; then \
	    echo "Container is running"; \
	else \
	    echo "Container is not running"; \
	    podman logs redis-cloud-run-testing-only; \
	    exit 1; \
	fi
	podman rm -f redis-cloud-run-testing-only;

pushimg-gcp: test
	@CURRENT_GPC_KEY=$$(gcloud auth print-access-token) && \
	podman login -u oauth2accesstoken --password $$CURRENT_GPC_KEY https://asia-east1-docker.pkg.dev 
	podman push redis-cloud-run:$(VERSION) asia-east1-docker.pkg.dev/my-journalist-fastapi/redis-service/redis-cloud-run:$(VERSION)

.PHONY: all buildimg test pushimg-gcp