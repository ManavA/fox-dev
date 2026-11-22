# Faster release builds for the eval (same code paths, no LTO): applied to agents and to grading alike.
export CARGO_PROFILE_RELEASE_LTO=off CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_PROFILE_RELEASE_INCREMENTAL=false
