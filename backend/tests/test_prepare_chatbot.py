import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.api import prepare_chatbot


def test_get_chatbot_regenerates_embeddings_when_folder_missing(monkeypatch, tmp_path):
    upload_file = tmp_path / "sample.pdf"
    upload_file.write_bytes(b"%PDF-1.4")

    embeddings_dir = tmp_path / "Embeddings"
    embeddings_dir.mkdir()

    monkeypatch.setattr(prepare_chatbot, "embeddings_folder_path", str(embeddings_dir))
    monkeypatch.setattr(prepare_chatbot, "settings", SimpleNamespace(model_name="test-model"))

    generated = {}

    def fake_generate_embeddings(file_path, embeddings_folder_path):
        generated["path"] = file_path
        dest = Path(embeddings_folder_path) / "sample"
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "index.faiss").write_text("dummy")

    monkeypatch.setattr(prepare_chatbot, "save_faiss_embeddings_file", fake_generate_embeddings)

    def fake_load_embeddings(embeddings_path):
        assert Path(embeddings_path).exists()
        return object()

    monkeypatch.setattr(prepare_chatbot, "load_faiss_embeddings_file", fake_load_embeddings)

    class DummyChatbot:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    monkeypatch.setattr(prepare_chatbot, "Chatbot", DummyChatbot)

    chatbot, session_id = prepare_chatbot.get_chatbot_for_user_selected_file(str(upload_file))

    assert chatbot is not None
    assert session_id
    assert generated["path"] == str(upload_file)
