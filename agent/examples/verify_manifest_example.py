"""Example script demonstrating how to build and verify a manifest using the agent tools."""
from agent.protect import build_manifest, save_manifest
from agent.agent import verify_manifest


def run_example():
    paths = ["./agent"]
    manifest = build_manifest(paths)
    save_manifest(manifest, "./agent/core_manifest.json")
    print("Saved manifest; now running verify from agent.agent:")
    verify_manifest()


if __name__ == "__main__":
    run_example()
