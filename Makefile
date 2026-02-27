SHELL := /usr/bin/env bash -o errexit -o pipefail -o nounset

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-23s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Images
.PHONY: image-compress
image-compress: ## Compress images
	find imgs/src -name '*' -type f | grep -v '.DS_Store' | xargs bash lib/scripts/image_processor.sh convert

.PHONY: image-upload
image-upload: ## Upload images
	node lib/scripts/upload_to_r2.js
