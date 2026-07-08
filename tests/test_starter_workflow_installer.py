from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).absolute().parents[1] / "scripts"))

import starter_workflow_installer as installer
from starter_workflow_installer import GitCommandResult


@pytest.fixture()
def isolated_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "ResearchLoop"
    root.mkdir()
    monkeypatch.setattr(installer, "ROOT", root)
    return root


def fake_git(ref: str = "8990143c3835f899e5331286a6a3b3393a2926ef", dirty: str = ""):
    calls: list[tuple[list[str], Path | None]] = []

    def runner(args: list[str], cwd: Path | None = None) -> GitCommandResult:
        calls.append((args, cwd))
        if args == ["rev-parse", "HEAD"]:
            return GitCommandResult(args, str(cwd or ""), 0, ref + "\n", "")
        if args == ["status", "--short"]:
            return GitCommandResult(args, str(cwd or ""), 0, dirty, "")
        return GitCommandResult(args, str(cwd or ""), 0, "", "")

    runner.calls = calls  # type: ignore[attr-defined]
    return runner


def test_missing_workflow_without_state_needs_prompt(isolated_root: Path) -> None:
    result = installer.status("nature-skills")

    assert result["installed"] is False
    assert result["needs_prompt"] is True
    assert result["local_path"].endswith(str(Path("external") / "nature-skills"))


@pytest.mark.parametrize("decision", ["skipped", "dismissed"])
def test_marked_workflow_suppresses_prompt(isolated_root: Path, decision: str) -> None:
    marked = installer.mark("nature-skills", decision)
    result = installer.status("nature-skills")

    assert marked["ok"] is True
    assert result["decision"] == decision
    assert result["needs_prompt"] is False


def test_existing_clone_reports_installed_ref(isolated_root: Path) -> None:
    clone = isolated_root / "external" / "nature-skills"
    (clone / ".git").mkdir(parents=True)
    runner = fake_git(ref="abc123")

    result = installer.status("nature-skills", runner=runner)

    assert result["installed"] is True
    assert result["current_ref"] == "abc123"
    assert result["needs_prompt"] is False


def test_install_dry_run_targets_external_clone(isolated_root: Path) -> None:
    result = installer.install("nature-skills", dry_run=True)

    assert result["ok"] is True
    assert result["dry_run"] is True
    commands = result["planned_commands"]
    assert commands[0]["command"].startswith("git clone --no-checkout")
    assert commands[0]["command"].endswith(str(isolated_root / "external" / "nature-skills"))
    assert commands[1]["command"] == "git checkout 8990143c3835f899e5331286a6a3b3393a2926ef"


def test_dirty_existing_clone_blocks_install_without_checkout(isolated_root: Path) -> None:
    clone = isolated_root / "external" / "nature-skills"
    (clone / ".git").mkdir(parents=True)
    runner = fake_git(dirty=" M skills/nature-writing/SKILL.md\n")

    result = installer.install("nature-skills", runner=runner)

    assert result["ok"] is False
    assert result["blocked_reason"] == "existing_clone_dirty"
    assert ["checkout", installer.WORKFLOWS["nature-skills"]["pinned_ref"]] not in [args for args, _cwd in runner.calls]  # type: ignore[attr-defined]
