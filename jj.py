import tempfile
from pathlib import Path
import subprocess
import dataclasses
import re
import textwrap

LONG_DESC = textwrap.dedent("""bak version 1
    
    This is an initial implementation, nothing fancy.
    It reads single file from the args list and backs it up.

    More fun stuff to come.""")


STATUS_PATTERN = re.compile(
    r"(Working copy (now at)?|Parent commit)\s*: ([a-z0-9]+) ([a-z0-9]+) (\(empty\) )?(.*)"
)

BAK_V1 = Path("bak/bak_v1.py").read_text()
BAK_V1_COMMENTS = Path("bak/bak_v1_comments.py").read_text()


@dataclasses.dataclass
class Commit:
    """
    Working copy : xvpztrxr 26d5ff49 (empty) (no description set)
    Parent commit: zzzzzzzz 00000000 (empty) (no description set)
    Working copy now at: xvpztrxr 4a3e4b50 (empty) xd
    Working copy : mnxsqnnr 24632532 bak version 1
    Working copy now at: mnxsqnnr 713abd34 ok
    Parent commit      : zzzzzzzz 00000000 (empty) (no description set)
    """

    change_id: str
    commit_hash: str
    description: str

    @classmethod
    def from_line(cls, line: str):
        match = STATUS_PATTERN.match(line)
        assert match is not None
        change_id = match.group(3)
        commit_hash = match.group(4)
        description = match.group(6)
        return cls(change_id, commit_hash, description)


def all_pairs(l):
    for i in range(len(l) - 1):
        for j in range(i + 1, len(l)):
            yield (l[i], l[j])


def starts_same_letter(c1, c2):
    return c1[0] == c2[0]


def create_temp_dir():
    temp_dir = tempfile.mkdtemp()
    return Path(temp_dir)


def run_command(command, cwd=None) -> tuple[str, str]:
    process = subprocess.run(command, cwd=cwd, capture_output=True, shell=True)
    return process.stdout.decode("utf-8").strip(), process.stderr.decode(
        "utf-8"
    ).strip()


def setup(temp_dir: str):
    run_command("jj git init", temp_dir)
    run_command("jj config set --repo user.email 'codelab@example.com'", temp_dir)
    run_command("jj config set --repo user.name 'Code Lab'", temp_dir)
    run_command("jj config set --user ui.paginate never", temp_dir)
    return


def jj_st(temp_dir: str) -> tuple[Commit, Commit]:
    status, _ = run_command("jj st", temp_dir)
    lines = status.split("\n")
    return Commit.from_line(lines[-1]), Commit.from_line(lines[-2])


def jj_describe(description: str, temp_dir: str) -> tuple[Commit, Commit]:
    _, status = run_command(f'jj describe -m "{description}"', temp_dir)
    lines = status.split("\n")
    return Commit.from_line(lines[-1]), Commit.from_line(lines[-2])


def jj_new(temp_dir: str) -> Commit:
    _, status = run_command("jj new", temp_dir)
    lines = status.split("\n")
    return Commit.from_line(lines[-2])


def main():
    while True:
        # I don't use the context manager because I want to control when I delete the dir
        temp_dir = tempfile.TemporaryDirectory(delete=False)

        # 2.1
        setup(temp_dir.name)

        # 2.2
        zero_commit, commit1 = jj_st(temp_dir.name)

        with (Path(temp_dir.name) / "bak.py").open("w") as file:
            file.write(BAK_V1)

        _, commit1_1 = jj_st(temp_dir.name)

        # 2.3
        _, commit1_2 = jj_describe("bak version 1", temp_dir.name)
        _ = run_command("jj describe -m 'bak version 1' --reset-author")  # bugfix
        _, commit1_3 = jj_describe(LONG_DESC, temp_dir.name)

        # 2.4
        commit2 = jj_new(temp_dir.name)
        _, commit2_1 = jj_describe("it's important to comment our code", temp_dir.name)
        with (Path(temp_dir.name) / "bak.py").open("w") as file:
            file.write(BAK_V1_COMMENTS)
        _, commit2_2 = jj_st(temp_dir.name)
        commit3 = jj_new(temp_dir.name)

        if any(
            starts_same_letter(c1, c2)
            for c1, c2 in all_pairs(
                [commit1.change_id, commit2.change_id, commit3.change_id]
            )
        ):
            print(commit3)
            print(commit2)
            print("\t", commit2_1)
            print("\t", commit2_2)
            print(commit1)
            print("\t", commit1_1)
            print("\t", commit1_2)
            print("\t", commit1_3)
            print(zero_commit)
            print(temp_dir.name)
            break
        temp_dir.cleanup()


if __name__ == "__main__":
    main()
    # print(Commit.from_line("Working copy : povmuuuz eb5c9869 (empty) (no description set)"))
