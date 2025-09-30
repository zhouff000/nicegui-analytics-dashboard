def load_css(file_path: str) -> str:
    with open(file_path) as f:
        return f"<style>{f.read()}</style>"
