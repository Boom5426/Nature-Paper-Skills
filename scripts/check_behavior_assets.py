#!/usr/bin/env python3
"""Validate evaluation assets only; this does not execute or grade an agent."""
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / 'evals/manifest.json').read_text())
    assert manifest['schema'] == 1
    assert (root / manifest['entry_skill']).is_file()
    ids = set()
    for case in manifest['cases']:
        assert case['id'] not in ids, 'duplicate case ID'
        ids.add(case['id'])
        path = (root / case['input']).resolve()
        assert root in path.parents and path.is_file()
        assert path.read_text().strip(), 'empty task'
        assert len(case['rubric']) >= 3 and all(isinstance(x, str) and x.strip() for x in case['rubric'])
    assert len(ids) >= 4
    print(f'{len(ids)} behavior case definitions validated; no model run or behavioral grade performed.')


if __name__ == '__main__':
    main()
