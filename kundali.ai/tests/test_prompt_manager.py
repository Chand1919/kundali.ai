from src.prompt_manager import PromptManager

def test_build_summary_prompt():
    pm = PromptManager()
    prompt = pm.build_summary_prompt({"name": "Project X"})
    assert "Project X" in prompt
