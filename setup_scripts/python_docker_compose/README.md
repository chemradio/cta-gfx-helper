<!-- User submitted -->

## STAGE1

# Layer 1

Specify Environment type. Can be AZURE, GITHUB_CODESPACES, LOCAL

# Layer 2

Specify if the DB should be erased and rebuilt

<!-- More specific config -->

## STAGE2

# Layer 3

Select if container code folders should be mounted to the local filesystem for advanced debugging

# Layer 4

Specify container names

# Layer 6

Specify container ports

<!-- Finish -->

# Layer 5

Specify in docker compose should start after compose-file is generated

<!-- Inner workings -->

# Layer

-   Gather environment variables and pass them to the container array
-   Open Template
-   Populate container names
-   Populate container ports
-   Add REBUILD_DB argument to dispatcher
-   Add volumes based on selected env type
-   Add dev volume mapping to local fs based on user choice
-   Populate container image names based on selected env type
