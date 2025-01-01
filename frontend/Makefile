VERSION:=0.1.2
all: buildimg test pushimg-gcp clean

buildimg:
	podman build -t my_journalist_app:$(VERSION) .;
	podman build -t my_journalist_app:latest .;

test: buildimg
	podman rm -f my_journalist_app > /dev/null || true;
	podman run -d --name my_journalist_app_testing_only -p 8080:8080 my_journalist_app:latest; 
	@sleep 10;
	@if podman ps --filter "name=my_journalist_app_testing_only" --format "{{.Names}}" | grep -q my_journalist_app_testing_only; then \
	    echo "Container is running"; \
	else \
	    echo "Container is not running"; \
	    podman logs my_journalist_app_testing_only; \
	    exit 1; \
	fi
	podman rm -f my_journalist_app_testing_only;

pushimg-gcp: test
	@CURRENT_GPC_KEY=$$(gcloud auth print-access-token) && \
	podman login -u oauth2accesstoken --password $$CURRENT_GPC_KEY asia-east1-docker.pkg.dev 
	podman push my_journalist_app:$(VERSION) asia-east1-docker.pkg.dev/my-journalist-fastapi/nextjs/my_journalist_app:$(VERSION)
	podman push my_journalist_app:latest asia-east1-docker.pkg.dev/my-journalist-fastapi/nextjs/my_journalist_app:latest

.PHONY = all buildimg test pushimg-gcp