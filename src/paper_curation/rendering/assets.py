"""Static assets used by generated pages."""

from importlib.resources import files


def load_text_asset() -> str:
    """Return the topic-page JavaScript bundled with this package."""
    return files("paper_curation.rendering.topic_page").joinpath("app.js").read_text(
        encoding="utf-8"
    )
