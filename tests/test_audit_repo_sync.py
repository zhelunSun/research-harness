from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.audit_repo_sync import audit_repository, exit_code, lfs_findings, parse_lfs_pending


def git(path: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(path), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if proc.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc.stdout.strip()


class SyncAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--bare", str(self.remote)], check=True, capture_output=True)
        self.work = self.root / "work"
        subprocess.run(["git", "init", str(self.work)], check=True, capture_output=True)
        git(self.work, "config", "user.name", "Sync Test")
        git(self.work, "config", "user.email", "sync-test@example.invalid")
        (self.work / "README.md").write_text("initial\n", encoding="utf-8")
        git(self.work, "add", "README.md")
        git(self.work, "commit", "-m", "initial")
        git(self.work, "branch", "-M", "main")
        git(self.work, "remote", "add", "origin", str(self.remote))
        git(self.work, "push", "-u", "origin", "main")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def audit(self, fetch: bool = False):
        return audit_repository(self.work, "test", "main", fetch)

    def test_clean_synced(self) -> None:
        result = self.audit()
        self.assertEqual(exit_code([result]), 0)
        self.assertEqual((result["behind"], result["ahead"], result["dirty"]), (0, 0, 0))

    def test_dirty_is_warning(self) -> None:
        (self.work / "README.md").write_text("dirty\n", encoding="utf-8")
        result = self.audit()
        self.assertEqual(exit_code([result]), 2)
        self.assertIn("dirty_worktree", {item["code"] for item in result["issues"]})

    def test_local_ahead_is_critical(self) -> None:
        (self.work / "local.txt").write_text("local\n", encoding="utf-8")
        git(self.work, "add", "local.txt")
        git(self.work, "commit", "-m", "local")
        result = self.audit()
        self.assertEqual(exit_code([result]), 1)
        self.assertEqual(result["ahead"], 1)

    def test_behind_and_diverged(self) -> None:
        other = self.root / "other"
        subprocess.run(["git", "clone", str(self.remote), str(other)], check=True, capture_output=True)
        git(other, "checkout", "main")
        git(other, "config", "user.name", "Sync Test")
        git(other, "config", "user.email", "sync-test@example.invalid")
        (other / "remote.txt").write_text("remote\n", encoding="utf-8")
        git(other, "add", "remote.txt")
        git(other, "commit", "-m", "remote")
        git(other, "push", "origin", "main")
        behind = self.audit(fetch=True)
        self.assertEqual(exit_code([behind]), 2)
        self.assertEqual(behind["behind"], 1)

        (self.work / "local.txt").write_text("local\n", encoding="utf-8")
        git(self.work, "add", "local.txt")
        git(self.work, "commit", "-m", "local")
        diverged = self.audit(fetch=True)
        self.assertEqual(exit_code([diverged]), 1)
        self.assertIn("diverged", {item["code"] for item in diverged["issues"]})

    def test_missing_upstream_and_deleted_remote_branch(self) -> None:
        git(self.work, "branch", "local-only")
        git(self.work, "switch", "local-only")
        no_upstream = self.audit()
        self.assertEqual(exit_code([no_upstream]), 1)
        self.assertIn("missing_upstream", {item["code"] for item in no_upstream["issues"]})

        git(self.work, "switch", "main")
        subprocess.run(
            ["git", "--git-dir", str(self.remote), "update-ref", "-d", "refs/heads/main"],
            check=True,
        )
        deleted = self.audit()
        self.assertEqual(exit_code([deleted]), 1)
        self.assertIn("remote_branch_deleted", {item["code"] for item in deleted["issues"]})

    def test_fetch_failure_is_warning(self) -> None:
        git(self.work, "remote", "set-url", "origin", str(self.root / "missing.git"))
        result = self.audit(fetch=True)
        self.assertEqual(exit_code([result]), 2)
        self.assertIn("fetch_failed", {item["code"] for item in result["issues"]})

    def test_lfs_parsing_and_failure(self) -> None:
        status = """Objects to be pushed to origin/main:\n\n\tasset.tif (LFS: abc -> File: def)\n\nObjects to be committed:\n"""
        self.assertEqual(len(parse_lfs_pending(status)), 1)
        findings = lfs_findings(status, 1, "pointer: missingObject: asset.tif")
        self.assertEqual(len(findings), 2)


if __name__ == "__main__":
    unittest.main()
