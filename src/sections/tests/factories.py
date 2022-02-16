from typing import Type
import pytest
from sections import Sections

@pytest.fixture
def make_section(*args):
    def _section(section_type: Type[Sections.Section], **kwargs) -> Sections.Section:
        if not issubclass(section_type, Sections.Section):
            raise TypeError(f'{section_type} cannot be a section')
        return section_type(*args, **kwargs)
    return _section

@pytest.fixture
def make_circular_section()

