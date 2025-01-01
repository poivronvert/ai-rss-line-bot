VERSION:=0.1.9
all: buildwhl buildimg test pushimg-gcp clean

buildwhl: 
	sed -i '' 's/version = ".*"/version = "$(VERSION)"/' pyproject.toml
	poetry build -o .tmp/

buildimg: buildwhl
	podman build --no-cache -t my_journalist:$(VERSION) .;
	podman build --no-cache -t my_journalist:latest .;

test: buildimg
	podman rm -f my_journalist_testing_only > /dev/null || true;
	podman run -d --name my_journalist_testing_only -p 38000:8000 my_journalist:latest; 
	@sleep 10;
	@if podman ps --filter "name=my_journalist_testing_only" --format "{{.Names}}" | grep -q my_journalist_testing_only; then \
	    echo "Container is running"; \
	else \
	    echo "Container is not running"; \
	    podman logs my_journalist_testing_only; \
	    exit 1; \
	fi
	podman rm -f my_journalist_testing_only;

pushimg-gcp: test
	@CURRENT_GPC_KEY=$$(gcloud auth print-access-token) && \
	podman login -u oauth2accesstoken --password $$CURRENT_GPC_KEY https://asia-east1-docker.pkg.dev 
	podman push my_journalist:$(VERSION) asia-east1-docker.pkg.dev/my-journalist-fastapi/mainapi/my-journalist:$(VERSION)
	podman push my_journalist:latest asia-east1-docker.pkg.dev/my-journalist-fastapi/mainapi/my-journalist:latest

clean: 
	rm -rf .tmp

.PHONY = all buildimg pushimg-gcp