from pathlib import Path

__all__ = ['root_path', 'test_path']

root_path = Path(__file__).parent.parent.parent
test_path = root_path / 'Tools/Python/test.txt'
