## Backlog
- AI diagnostics
- Kubernetes checks
- Docker checks

## In Progress
- Unit tests
- GitHub Actions

## Review
- README improvements

## Done
- CPU module
- Memory module
- Disk module
- Logging
- CLI


## Future 

- Docker reclaimable space. Dangling images, build cache, stopped containers, orphaned volumes. "Docker is using 47 GB, 31 GB reclaimable." People love a tool that hands back disk space — it's the most immediately visible win you can offer.

- Snapshot and diff. Record a known-good state, then answer "what changed since it last worked?" This upgrades your Milestone 6 compare from a reporting feature into a debugging feature, which is a much better pitch.

- Clock drift. Check NTP sync and skew. Clock drift silently breaks TLS handshakes, JWT validation, AWS request signing, and Kerberos — and it produces error messages that point nowhere near the real cause. Cheap to implement, and the one time it fires you've saved someone an entire afternoon.

- Port conflicts. <name> ports — what's holding :3000, :5432, :8080, with the owning process and an offer to kill it. Tiny to build, and it's a daily annoyance for every developer alive.

- Toolchain drift vs. the project. Read .tool-versions, .nvmrc, .python-version, go.mod, and terraform's required_version, then compare against what's actually installed. "This repo wants Terraform 1.9, you have 1.5." This is your killer feature — it's the number one cause of "works on my machine," nothing owns it cleanly, and it's the thing platform teams would pay to enforce across a fleet. I'd move it ahead of everything in Milestone 5.