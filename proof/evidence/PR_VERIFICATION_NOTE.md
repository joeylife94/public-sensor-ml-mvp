# PR Verification Note

This pull request is used as the executable acceptance gate for the final Docker verification workflow.

Expected CI path:

1. install project and test dependencies;
2. run automated tests;
3. generate a small public-contract-compatible synthetic fixture;
4. build the Docker image;
5. start the container with the fixture mounted read-only;
6. verify `/health` returns success;
7. verify the buyer-facing dashboard renders expected proof markers.

No production or client data is used by CI. Real S-DoT evidence remains separately recorded under `proof/evidence/`.
